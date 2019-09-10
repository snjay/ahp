from ahp import AHP

alts = ['Pizza Hut', "Domino's"]
crits = ['Distance', 'Price', 'Cuisine']
goal = 'Picking where to eat'

decision_maker = AHP(alternatives=alts, criterias=crits, goal=goal)
print(decision_maker)
print(decision_maker.best_decision())