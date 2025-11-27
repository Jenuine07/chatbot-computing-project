# # pipeline/hybrid_router.py

# """
# Hybrid Router
# - Detect intent
# - Route to correct pipeline (currently only RAG)
# """

# from nlp.intent_detector import detect_intent
# from pipeline.rag_pipeline import run_rag_pipeline

# def answer_query(query: str) -> str:
#     intent = detect_intent(query)

#     # For now: only RAG is active
#     if intent == "RAG":
#         return run_rag_pipeline(query)
#     else:
#         # Fallback: still send to RAG until SQL pipeline is ready
#         return run_rag_pipeline(query)
