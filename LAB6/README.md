# Lab 6 - NLP Fundamentals: Tokenization, Embeddings & Chunking
All documents are synthetic teaching data (not real policies). Model: sentence-transformers/all-MiniLM-L6-v2 (CPU).

## Setup
    python -m venv .venv
    .venv\Scripts\Activate.ps1        # macOS/Linux: source .venv/bin/activate
    python -m pip install numpy scikit-learn sentence-transformers
    python -m pip freeze > requirements.txt
    python create_dataset.py          # once; creates corpus.json and queries.json

## Task 1
    python task1_tokens.py
    python guided_chatbot.py
    python task1_chatbot_check.py

## Task 2
    python task2_chunks.py            # tests
    python task2_compare.py
    python task2_paraphrase.py
    python guided_embeddings.py
    python guided_suggestions.py embedding

## Task 3
    python task3_retrieval.py         # add --no-embedding if the model cannot be downloaded
    python document_chatbot.py

## Other
lab6_search.py, scenario1..5 scripts, guided_tokens/chunks/limits/metrics.py
Libraries: numpy, scikit-learn, sentence-transformers. Reference code adapted from the lab manual; corpus and extra scripts are my own.
