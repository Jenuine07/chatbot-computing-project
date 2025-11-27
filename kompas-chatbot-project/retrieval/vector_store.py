# retrieval/vector_store.py

import pyarrow.parquet as pq
import pandas as pd
import pyarrow.dataset as ds
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from retrieval.embedder import embed_batch
from config.settings import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, EMB_DIM, DATASET_PATH, MASTER_LOC_PATH
from typing import List, Optional
from qdrant_client.http.models import Filter

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def search(query_vector: List[float], qdrant_filter: Optional[Filter] = None, top_k: int = 5):
    try:
        search_result = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            query_filter=qdrant_filter,
            limit=top_k,
            with_payload=True 
        )
        return search_result
    except Exception as e:
        print(f"🚨 Error during Qdrant search: {e}")
        return []
    
def create_collection_if_missing(recreate: bool = False):
    if recreate:
        print(f"⚠️ Recreating collection: {COLLECTION_NAME}")
        try:
            client.recreate_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=rest.VectorParams(
                    size=EMB_DIM,
                    distance=rest.Distance.COSINE
                ),
            )
            print("✅ Collection recreated successfully.")
        except Exception as e:
            print(f"🚨 Error recreating collection: {e}")
    else:
        try:
            client.get_collection(collection_name=COLLECTION_NAME)
            print(f"✅ Collection '{COLLECTION_NAME}' already exists.")
        except Exception:
            print(f"Collection '{COLLECTION_NAME}' not found. Creating new one...")
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=rest.VectorParams(
                    size=EMB_DIM,
                    distance=rest.Distance.COSINE
                ),
            )
            print("✅ Collection created successfully.")

def collection_has_points() -> bool:
    try:
        count = client.count(collection_name=COLLECTION_NAME)
        return count.count > 0
    except Exception:
        return False

def upsert_vectors(vectors, payloads, batch_size=32):
    from qdrant_client.http import models as rest

    n = len(vectors)
    for i in range(0, n, batch_size):
        end = min(n, i + batch_size)
        points = [
            rest.PointStruct(
                id=str(uuid.uuid4()),
                vector=vectors[j],
                payload=payloads[j],
            )
            for j in range(i, end)
        ]
        client.upsert(collection_name=COLLECTION_NAME, points=points)

    print(f"✅ Upserted {n} vectors into {COLLECTION_NAME}")

def create_embeddings_if_missing(force=False, batch_rows=128): 
    from retrieval.vector_store import collection_has_points
    if not force and collection_has_points():
        print("⚡ Embeddings already exist in Qdrant → skipping.")
        return

    if force:
        print("⚠️ Force option is True. Recreating collection.")


    try:
        loc_df = pd.read_excel(MASTER_LOC_PATH)
        for col in ["provinsi", "kabkot"]:
            loc_df[col] = loc_df[col].astype(str).str.strip().str.lower()
        loc_df = loc_df[["provinsi", "kabkot"]].drop_duplicates()
        print(f"✅ Loaded location master data with {len(loc_df)} rows.")
    except FileNotFoundError:
        print(f"🚨 Error: Master location file not found at {MASTER_LOC_PATH}")
        return

    dataset = ds.dataset(DATASET_PATH, format="parquet")

    inserted = 0
    print("⚡ Embedding in streaming mode...")

    required_cols = [
        "judul_asli", "judul_bersih", "jenis_peraturan", "nama_daerah",
        "nomor", "tahun", "tentang", "kategori_final", "Link Final", 
        "body",
    ]

    for batch_idx, record_batch in enumerate(dataset.to_batches(batch_size=batch_rows, columns=required_cols)):
        df = record_batch.to_pandas()

        rename_map = {
            "judul_bersih": "judul_bersih",
            "kategori_final": "kategori",
            "Link Final": "link_final",
        }
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

        df["nama_daerah"] = df["nama_daerah"].astype(str).str.strip().str.lower()
        df = df.merge(loc_df, left_on="nama_daerah", right_on="kabkot", how="left")
        df['provinsi'] = df['provinsi'].fillna('unknown') 

        df = df.fillna("")
        texts = (df["judul_bersih"].astype(str) + " " + df["tentang"].astype(str)).tolist()
        vectors = embed_batch(texts)

        payload_cols = [
            "judul_asli", "judul_bersih", "jenis_peraturan", "nama_daerah",
            "nomor", "tahun", "tentang", "kategori", "link_final", 
            # "body", "provinsi"
        ]
        for col in payload_cols:
            if col not in df.columns:
                df[col] = ""

        df["body_preview"] = df["body"].str[:200000]
        
        payloads = df[payload_cols + ["body_preview"]].to_dict(orient="records")

        points = [
            rest.PointStruct(
                id=str(uuid.uuid4()),
                vector=vec,
                payload=pay
            )
            for vec, pay in zip(vectors, payloads)
        ]

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
            wait=False 
        )

        inserted += len(df)
        print(f"✅ Upserted Batch {batch_idx + 1}: {len(df)} rows (total {inserted})")

        del df, texts, vectors, payloads, points

    print(f"🎯 Done. Total inserted: {inserted}")
