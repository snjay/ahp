from ahp import AHP

if __name__ == "__main__":
    ASK_QUESTIONS = False

    # Main objective/goal to be achieved
    goal = "Deciding where to eat"

    # The alternatives (final decisions)
    alternatives = [
        "Pizza Hut", 
        "Domino's"
    ]

    # The criterias to judge the alternatives
    criterias = [
        "Distance", 
        "Price", 
        "Cuisine"
    ]

    ahp_decider = AHP(alternatives, criterias, goal)

    if ASK_QUESTIONS:
        # Baseline prioritisation walk through (prints out questions in terminal)
        ahp_decider.prioritise()
    else:
        # Add your prioritisations
        ahp_decider.compare_alternatives_wrt_criteria(alternatives=(0, 1), criteria=0, multiple=5)
        ahp_decider.compare_criterias_wrt_goal(criterias=(1, 2), multiple=5)
        pass

    # Returns the index of alternatives array
    # that is the best result (based on the
    # prior comparisons made)
    result = ahp_decider.decide()

    print(alternatives[result])