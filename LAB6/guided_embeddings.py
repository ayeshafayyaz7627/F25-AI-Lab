import numpy as np
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
passages = ["Reset a forgotten password using the recovery link.",
            "Submit assignments through the learning portal.",
            "Check ink levels when a printer produces blank pages."]
C = model.encode(passages, normalize_embeddings=True)
for q_text in ["How can I recover my login?", "I do not need a password reset"]:
    Q = model.encode([q_text], normalize_embeddings=True)
    scores = (Q @ C.T)[0]
    print("\nQuery:", q_text, "| Embedding shape:", C.shape)
    for i in np.argsort(-scores):
        print(i, round(float(scores[i]), 3), passages[i])
assert np.allclose(np.linalg.norm(C, axis=1), 1, atol=1e-5)
