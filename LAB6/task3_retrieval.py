"""Task 3: evaluate 3 chunking strategies x 2 retrieval methods. Use --no-embedding if the model is unavailable."""
import argparse, csv, json, time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from task2_chunks import make_chunks


def rank_list(row, chunks, q):
    top = np.argsort(-row, kind="stable")[:3]
    good = [r for r, i in enumerate(top, 1)
            if chunks[i]["doc"] == q["doc"] and q["evidence"] in chunks[i]["text"]]
    return top, good


def evaluate(scores, chunks, items, failures, label):
    hits, rr = [], []
    for row, q in zip(scores, items):
        if q["doc"] is None:
            continue
        top, good = rank_list(row, chunks, q)
        hits.append(bool(good)); rr.append(1 / good[0] if good else 0)
        if not good:
            failures.append((label, q["query"], chunks[top[0]]["id"], chunks[top[0]]["text"][:120]))
    return (float(np.mean(hits)), float(np.mean(rr))) if hits else (None, None)


def main(skip_embedding):
    docs = json.load(open("corpus.json", encoding="utf-8"))
    items = json.load(open("queries.json", encoding="utf-8"))
    for q in items:
        assert q["split"] in {"dev", "test"}
        if q["doc"] is not None:
            assert q["evidence"] and q["evidence"] in docs[q["doc"]]
    query_texts = [q["query"] for q in items]
    model = None
    if not skip_embedding:
        from sentence_transformers import SentenceTransformer
        t = time.perf_counter()
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
        print("Model load seconds", round(time.perf_counter() - t, 3))
    logs, summary, failures = [], [], []
    for strategy in ["0", "10", "sentence"]:
        chunks = make_chunks(docs, strategy)
        texts = [c["text"] for c in chunks]
        if model:
            lengths = [len(model.tokenizer(t, truncation=False)["input_ids"]) for t in texts + query_texts]
            print(f"[{strategy}] max token length {max(lengths)} / limit {model.max_seq_length}")
            if max(lengths) > model.max_seq_length:
                raise ValueError("Model limit exceeded; rechunk or shorten query")
        for method in ["tfidf"] + ([] if skip_embedding else ["embedding"]):
            t = time.perf_counter()
            if method == "tfidf":
                vec = TfidfVectorizer(); C = vec.fit_transform(texts); Q = vec.transform(query_texts)
            else:
                C = model.encode(texts, normalize_embeddings=True)
                Q = model.encode(query_texts, normalize_embeddings=True)
            enc = time.perf_counter() - t
            t = time.perf_counter()
            scores = (Q @ C.T).toarray() if method == "tfidf" else Q @ C.T
            srch = time.perf_counter() - t
            for split in ["dev", "test"]:
                idx = [i for i, q in enumerate(items) if q["split"] == split]
                label = f"{strategy}/{method}/{split}"
                hit, mrr = evaluate(scores[idx], chunks, [items[i] for i in idx], failures, label)
                summary.append(dict(strategy=strategy, method=method, split=split, hit3=hit, mrr3=mrr,
                                    chunks=len(chunks), encode_s=round(enc, 4), search_s=round(srch, 5)))
                print(label, "Hit@3", hit, "MRR@3", None if mrr is None else round(mrr, 3),
                      "chunks", len(chunks), "encode_s", round(enc, 4), "search_s", round(srch, 5))
            for row, q in zip(scores, items):
                for rank, i in enumerate(np.argsort(-row, kind="stable")[:3], 1):
                    c = chunks[i]
                    logs.append(dict(strategy=strategy, method=method, query=q["query"], split=q["split"],
                                     rank=rank, score=float(row[i]), chunk_id=c["id"], doc=c["doc"],
                                     start=c["start"], end=c["end"], text=c["text"],
                                     answerable=q["doc"] is not None))
                if q["doc"] is None:
                    print(f"   unanswerable {q['query']!r} top1 {chunks[np.argmax(row)]['id']} score {row.max():.3f}")
    with open("retrieval_log.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(logs[0])); w.writeheader(); w.writerows(logs)
    with open("results_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0])); w.writeheader(); w.writerows(summary)
    print("\nFAILURES (query had no relevant chunk in top 3):")
    for label, q, cid, txt in failures:
        print(f"- {label} | {q!r} | top1 {cid} | {txt}")
    print("\nWrote retrieval_log.csv and results_summary.csv")


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--no-embedding", action="store_true")
    main(p.parse_args().no_embedding)
