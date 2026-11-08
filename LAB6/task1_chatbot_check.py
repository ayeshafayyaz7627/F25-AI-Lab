from guided_chatbot import build_bot, reply
engine = build_bot()
assert "it_help.txt" in reply(engine, "How do I reset my password?")
assert reply(engine, "") == "Please enter a question."
assert "No matching FAQ" in reply(engine, "volcano geology")
assert "Possible matches" in reply(engine, "password recovery")
# transcript for the report
for q in ["How do I reset my password?", "password recovery", "", "volcano geology",
          "What should I do if the printer prints blank pages?"]:
    print("You:", repr(q)); print("Bot:", reply(engine, q)); print()
print("FAQ behaviour checks passed")
