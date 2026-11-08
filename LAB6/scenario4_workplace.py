from lab6_search import Retriever, show_hits
records = [
{"id":"remote:staff", "audience":"employee",
 "text":"Employees may request remote work with manager approval."},
{"id":"remote:contractor", "audience":"contractor",
 "text":"Contractors may work remotely only when the signed contract "
 "explicitly permits remote work."}]
engine = Retriever(records)
show_hits(engine.search("remote work", k=1, filters={"audience":"contractor"}))
print("\n-- without filter (risk: employee rule can rank first)")
show_hits(engine.search("remote work", k=2))
