import re

samples = [
    "AI, search!",              # punctuation
    "I can't log in.",          # contraction
    "help@example.com",         # email
    "CS4944 late submission",   # identifier
    "",                         # empty
    "یہ ایک مثال ہے",             # Urdu
]

for text in samples:
    ws = text.split()
    words = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
    print("Original  :", repr(text))
    print("Whitespace:", ws, len(ws))
    print("Word-like :", words, len(words))
    print()

assert re.findall(r"\b\w+\b", "") == []

# Optional: model (sub-word) tokenizer for two English examples
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
    for text in ["I can't log in.", "CS4944 help@example.com"]:
        toks = model.tokenizer.tokenize(text)
        print("Model sub-words:", repr(text), toks, len(toks))
except Exception as e:
    print("Model tokenizer unavailable:", e)

# Normalization risk demo: lowercasing/regex destroys identifiers and negation context
for t in ["POST /v2/token/refresh", "Do NOT share refresh_token"]:
    print(repr(t), "->", re.findall(r"\b\w+\b", t.lower()))
