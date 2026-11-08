from sentence_transformers import SentenceTransformer
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
for label, text in [("short", "Reset my password."), ("long", "password " * 300),
                    ("identifier", "CS4944 help@example.com /v2/token/refresh")]:
    ids = model.tokenizer(text, truncation=False)["input_ids"]
    print(label, "whitespace words:", len(text.split()), "tokens:", len(ids),
          "limit:", model.max_seq_length, "fits:", len(ids) <= model.max_seq_length)
