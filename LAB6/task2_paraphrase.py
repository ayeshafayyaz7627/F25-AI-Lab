"""Three paraphrased queries: TF-IDF vs embeddings on chunk records (sentence strategy)."""
import json
from task2_chunks import make_chunks
from lab6_search import Retriever

docs = json.load(open("corpus.json", encoding="utf-8"))
records = make_chunks(docs, "sentence")
queries = ["How can I regain access to my account?",
           "I was sick, how do I get more time?",
           "Where do I hand in my coursework?"]
for backend in ["tfidf", "embedding"]:
    try:
        engine = Retriever(records, backend)
    except Exception as e:
        print(backend, "unavailable:", e); continue
    for q in queries:
        print(f"\n[{backend}] {q}")
        hits = engine.search(q, k=3)
        if not hits: print("  no matches")
        for r, s in hits:
            print(f"  {r['id']} {s:.3f} chars {r['start']}-{r['end']}: {r['text'][:90]}...")
