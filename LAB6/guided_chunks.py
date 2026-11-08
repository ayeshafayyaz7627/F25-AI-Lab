from task2_chunks import windows, sentence_chunks
text = ("Late work is penalized. Illness may qualify for an extension "
        "when medical evidence is provided. Ask the coordinator first.")
for size in (12, 20):
    for name, spans in [("word windows", windows(text, size=size, overlap=4)),
                        ("sentence aware", sentence_chunks(text, size=size))]:
        print(f"{name} (size={size})")
        for start, end in spans:
            print(start, end, repr(text[start:end]))
            assert 0 <= start < end <= len(text)
