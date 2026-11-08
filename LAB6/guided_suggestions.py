import sys
from guided_chatbot import build_bot
backend = sys.argv[1] if len(sys.argv) > 1 else "tfidf"
engine = build_bot(backend)
for query in ["assignment upload", "forgot login"]:
    print(f"\nSuggested questions for {query!r} ({backend}):")
    for record, score in engine.search(query, k=3):
        if backend == "embedding" or score > 0:
            print(record["question"], f"({score:.3f})")
