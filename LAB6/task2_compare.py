"""Compare chunking strategies: counts, sizes, duplication, rule/exception survival."""
import json
from task2_chunks import make_chunks

docs = json.load(open("corpus.json", encoding="utf-8"))
items = [q for q in json.load(open("queries.json", encoding="utf-8")) if q["doc"]]
evidence = {q["doc"]: q["evidence"] for q in items}
orig_words = {d: len(t.split()) for d, t in docs.items()}

print(f"{'strategy':10} {'chunks':>6} {'avg_words':>9} {'dup_words':>9} {'evidence_intact':>15}")
for strategy in ["0", "10", "sentence"]:
    chunks = make_chunks(docs, strategy)
    sizes = [len(c["text"].split()) for c in chunks]
    dup = sum(sizes) - sum(orig_words.values())
    intact = sum(any(evidence[d] in c["text"] for c in chunks if c["doc"] == d)
                 for d in evidence)
    print(f"{strategy:10} {len(chunks):>6} {sum(sizes)/len(sizes):>9.1f} {dup:>9} {intact:>9}/{len(evidence)}")
    for d in evidence:
        if not any(evidence[d] in c["text"] for c in chunks if c["doc"] == d):
            print("   split evidence ->", d)
