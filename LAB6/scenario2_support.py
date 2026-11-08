from lab6_search import Retriever, show_hits
records = [
{"id":"returns:damage", "region":"PK",
 "text":"For a damaged parcel, contact support within 48 hours "
 "and attach photographs of the item and packaging."},
{"id":"returns:change", "region":"PK",
 "text":"For a change of mind, return unused items within 14 days."},
{"id":"returns:damage:other", "region":"OTHER",
 "text":"Damaged parcel reports in the other region have a 72 hour window."}]
engine = Retriever(records)
show_hits(engine.search("damaged parcel photographs", k=1, filters={"region":"PK"}))
print("\n-- without filter")
show_hits(engine.search("damaged parcel photographs", k=3))
for backend in ["tfidf", "embedding"]:
    try:
        e = Retriever(records, backend)
        print("\n--", backend, "'My parcel arrived broken'")
        show_hits(e.search("My parcel arrived broken", k=3))
    except Exception as ex:
        print("\n--", backend, "unavailable:", ex)
