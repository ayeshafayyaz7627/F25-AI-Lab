from lab6_search import Retriever, show_hits
records = [
{"id":"auth:v2", "version":"v2",
 "text":"Renew an expired API token with POST /v2/token/refresh. "
 "Send the refresh_token field; never print its value in logs."},
{"id":"auth:v1", "version":"v1",
 "text":"Renew an expired API token with POST /v1/auth/renew."}]
engine = Retriever(records)
show_hits(engine.search("renew expired API token", k=1, filters={"version":"v2"}))
print("\n-- v1"); show_hits(engine.search("renew expired API token", k=1, filters={"version":"v1"}))
print("\n-- v3 (nonexistent)"); show_hits(engine.search("renew expired API token", k=1, filters={"version":"v3"}))
