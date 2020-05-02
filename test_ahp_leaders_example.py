from ahp import AHP
import numpy as np
import pytest

# https://en.wikipedia.org/wiki/Analytic_hierarchy_process_%E2%80%93_leader_example
@pytest.fixture
def alts():
    return ["Tom", "Dick", "Harry"]

@pytest.fixture
def crits():
    return ["Experience", "Education", "Charisma", "Age"]

@pytest.fixture
def goal():
    return "Choose the most suitable leader"

# @pytest.mark.parametrize("test_input, expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
# def test_computes_correct_criteria_priority_matrix(alts, crits, goal):
#     decider = AHP(alternatives=alts, criterias=crits, goal=goal)
#     # Compare alternatives against a criteria
#     decider.compare_alternatives_wrt_criteria(alternatives=(0, 1), criteria=0, multiple=4)
#     decider.compare_alternatives_wrt_criteria(alternatives=(0, 2), criteria=0, multiple=1/4)
#     decider.compare_alternatives_wrt_criteria(alternatives=(1, 2), criteria=0, multiple=1/9)
#     np.testing.assert_array_equal(decider.crit_mat[0], [[1, 1/4, 4], [4, 1, 9], [1/4, 1/9, 1]])

def test_computes_correct_priority_matrix_for_experience(alts, crits, goal):
    decider = AHP(alternatives=alts, criterias=crits, goal=goal)
    # Experience
    decider.compare_alternatives_wrt_criteria(alternatives=(0, 1), criteria=0, multiple=1/4)
    decider.compare_alternatives_wrt_criteria(alternatives=(0, 2), criteria=0, multiple=4)
    decider.compare_alternatives_wrt_criteria(alternatives=(1, 2), criteria=0, multiple=9)
    np.testing.assert_array_equal(decider.crit_mat[0], [[1, 1/4, 4], [4, 1, 9], [1/4, 1/9, 1]])


def test_computes_correct_priority_matrix_for_education(alts, crits, goal):
    decider = AHP(alternatives=alts, criterias=crits, goal=goal)
    # Education
    decider.compare_alternatives_wrt_criteria(alternatives=(0, 1), criteria=1, multiple=3)
    decider.compare_alternatives_wrt_criteria(alternatives=(0, 2), criteria=1, multiple=1/5)
    decider.compare_alternatives_wrt_criteria(alternatives=(1, 2), criteria=1, multiple=1/7)
    np.testing.assert_array_equal(decider.crit_mat[1], [[1, 3, 1/5], [1/3, 1, 1/7], [5, 7, 1]])


def test_computes_correct_priority_matrix_for_charisma(alts, crits, goal):
    decider = AHP(alternatives=alts, criterias=crits, goal=goal)
    # Charisma
    decider.compare_alternatives_wrt_criteria(alternatives=(0, 1), criteria=2, multiple=5)
    decider.compare_alternatives_wrt_criteria(alternatives=(0, 2), criteria=2, multiple=9)
    decider.compare_alternatives_wrt_criteria(alternatives=(1, 2), criteria=2, multiple=4)
    np.testing.assert_array_equal(decider.crit_mat[2], [[1, 5, 9], [1/5, 1, 4], [1/9, 1/4, 1]])


def test_computes_correct_priority_matrix_for_age(alts, crits, goal):
    decider = AHP(alternatives=alts, criterias=crits, goal=goal)
    # Age
    decider.compare_alternatives_wrt_criteria(alternatives=(0, 1), criteria=3, multiple=1/3)
    decider.compare_alternatives_wrt_criteria(alternatives=(0, 2), criteria=3, multiple=5)
    decider.compare_alternatives_wrt_criteria(alternatives=(1, 2), criteria=3, multiple=9)
    np.testing.assert_array_equal(decider.crit_mat[3], [[1, 1/3, 5], [3, 1, 9], [1/5, 1/9, 1]])


def test_computes_correct_priority_matrix_for_goal(alts, crits, goal):
    decider = AHP(alternatives=alts, criterias=crits, goal=goal)
    # Criterias vs goal
    decider.compare_criterias_wrt_goal(criterias=(0, 1), multiple=4)
    decider.compare_criterias_wrt_goal(criterias=(0, 2), multiple=3)
    decider.compare_criterias_wrt_goal(criterias=(0, 3), multiple=7)
    decider.compare_criterias_wrt_goal(criterias=(1, 2), multiple=1/3)
    decider.compare_criterias_wrt_goal(criterias=(1, 3), multiple=3)
    decider.compare_criterias_wrt_goal(criterias=(3, 2), multiple=1/5)
    np.testing.assert_array_equal(decider.goal_mat, [[1, 4, 3, 7], [1/4, 1, 1/3, 3], [1/3, 3, 1, 5], [1/7, 1/3, 1/5, 1]])


def test_computes_correct_priority_vecs(alts, crits, goal):
    decider = AHP(alternatives=alts, criterias=crits, goal=goal)
    # Experience
    decider.compare_alternatives_wrt_criteria(alternatives=(0, 1), criteria=0, multiple=1/4)
    decider.compare_alternatives_wrt_criteria(alternatives=(0, 2), criteria=0, multiple=4)
    decider.compare_alternatives_wrt_criteria(alternatives=(1, 2), criteria=0, multiple=9)
    # Education
    decider.compare_alternatives_wrt_criteria(alternatives=(0, 1), criteria=1, multiple=3)
    decider.compare_alternatives_wrt_criteria(alternatives=(0, 2), criteria=1, multiple=1/5)
    decider.compare_alternatives_wrt_criteria(alternatives=(1, 2), criteria=1, multiple=1/7)
    # Charisma
    decider.compare_alternatives_wrt_criteria(alternatives=(0, 1), criteria=2, multiple=5)
    decider.compare_alternatives_wrt_criteria(alternatives=(0, 2), criteria=2, multiple=9)
    decider.compare_alternatives_wrt_criteria(alternatives=(1, 2), criteria=2, multiple=4)
    # Age
    decider.compare_alternatives_wrt_criteria(alternatives=(0, 1), criteria=3, multiple=1/3)
    decider.compare_alternatives_wrt_criteria(alternatives=(0, 2), criteria=3, multiple=5)
    decider.compare_alternatives_wrt_criteria(alternatives=(1, 2), criteria=3, multiple=9)
    # Criterias vs goal
    decider.compare_criterias_wrt_goal(criterias=(0, 1), multiple=4)
    decider.compare_criterias_wrt_goal(criterias=(0, 2), multiple=3)
    decider.compare_criterias_wrt_goal(criterias=(0, 3), multiple=7)
    decider.compare_criterias_wrt_goal(criterias=(1, 2), multiple=1/3)
    decider.compare_criterias_wrt_goal(criterias=(1, 3), multiple=3)
    decider.compare_criterias_wrt_goal(criterias=(3, 2), multiple=1/5)

    assert decider.decide() == 1