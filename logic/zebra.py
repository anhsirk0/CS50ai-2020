from logic import *

def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge, symbol):
            print(f"{symbol}: YES")
        elif not model_check(knowledge, Not(symbol)):
            print(f"{symbol}: MAYBE")

colors = [
    "red",
    "blue",
    "green",
    "white",
    "yellow"
]
rain = Symbol("rain")
walk = Symbol("walk")
home = Symbol("stay home")

knowledge = And(
    Implication(Not(rain), walk),
    Or(walk, home),
    Not(And(walk, home)),
    home
)

symbols = [rain , walk , home]

# print(knowledge.formula())

check_knowledge(knowledge)
print(model_check(knowledge, rain))

