from ahp import AHP

if __name__ == "__main__":

    # Define alternatives, criterias and goal
    goal = "Deciding where to eat"
    alternatives = [
        "Pizza Hut", 
        "Domino's"
    ]
    criterias = [
        "Distance", 
        "Price", 
        "Cuisine"
    ]

    decider = AHP(alternatives, criterias, goal)
    result = decider.decide()
    print(result)