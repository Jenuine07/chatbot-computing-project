# database/excel_loader.py

import pandas as pd
from config.settings import DATASET_PATH, MASTER_LOC_PATH


def load_dataset():
    df = pd.read_parquet(DATASET_PATH)

    rename_map = {
        "Nomor Baris Asli": "id",
        "judul_asli": "judul_asli",
        "judul_bersih": "judul_bersih",
        "jenis_peraturan": "jenis_peraturan",
        "nama_daerah": "nama_daerah",
        "nomor": "nomor",
        "tahun": "tahun",
        "tentang": "tentang",
        "Link Final": "link_final",
        "kategori_final": "kategori",
        "body": "body",
    }

    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    drop_cols = [col for col in df.columns if "link" in col.lower() and col.lower() != "link_final"]
    df = df.drop(columns=drop_cols, errors="ignore")

    if "tahun" in df.columns:
        df["tahun"] = pd.to_numeric(df["tahun"], errors="coerce").astype("Int64")
    if "nomor" in df.columns:
        df["nomor"] = df["nomor"].astype(str)

    for col in ["kategori", "jenis_peraturan", "nama_daerah"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()

    loc_df = pd.read_excel(MASTER_LOC_PATH)

    for col in ["provinsi", "kabkot", "kecamatan", "kelurahan"]:
        loc_df[col] = loc_df[col].astype(str).str.strip().str.lower()

    df = df.merge(loc_df[["provinsi", "kabkot"]], left_on="nama_daerah", right_on="kabkot", how="left")

    df["teks"] = df["judul_bersih"].fillna('') + ' ' + df["body"].fillna('')

    print(f"[excel_loader] Memuat {len(df)} baris, kolom: {df.columns.tolist()}")
    return df

def ambil_titik(provinsi: str, tahun: int, kategori: str):
    df = load_dataset()
    baris = df[
        (df["provinsi"] == provinsi.lower()) &
        (df["tahun"] == tahun) &
        (df["kategori"] == kategori.lower())
    ]
    if baris.empty:
        return None
    return baris.to_dict(orient="records")


def ambil_rentang(provinsi: str, rentang_tahun: tuple, kategori: str):
    mulai, akhir = rentang_tahun
    df = load_dataset()
    baris = df[
        (df["provinsi"] == provinsi.lower()) &
        (df["tahun"].between(mulai, akhir)) &
        (df["kategori"] == kategori.lower())
    ]
    if baris.empty:
        return []
    return baris.sort_values("tahun").to_dict(orient="records")
