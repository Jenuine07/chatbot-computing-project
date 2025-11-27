from fastapi import FastAPI, Request
from pipeline import rag_pipeline
import uvicorn

app = FastAPI()

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    query = body.get("query")
    top_k = body.get("top_k", 10)
    result = rag_pipeline.run_rag_pipeline(query, top_k)
    return {"answer": result}

@app.post("/embed")
async def embed(request: Request):
    body = await request.json()
    text = body.get("text")
    from retrieval.vector_store import embed_text
    embedding = embed_text(text)
    return {"embedding": embedding.tolist()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
