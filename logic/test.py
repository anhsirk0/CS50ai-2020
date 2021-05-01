from logic import *

rain = Symbol("rain")
walk = Symbol("walk")
home = Symbol("stay home")

knowledge = And(
    Implication(Not(rain), walk),
    Or(walk, home),
    Not(And(walk, home)),
    home
)
print(knowledge.formula())

print(model_check(knowledge, rain))

