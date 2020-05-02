from fractions import Fraction
from numpy import linalg as LA
import numpy as np

# Set printing options precision
# np.set_printoptions(precision=5)
# np.set_printoptions(formatter={'float': '{: 0.2f}'.format})

# Define alternatives, criterias and goal
alts = ['Pizza Hut', "Domino's"]
crits = ['Distance', 'Price', 'Cuisine']
goal = 'Picking where to eat'

# Init setup
nA, nC = len(alts), len(crits)
crit_mat = {}
for c in crits:
    crit_mat[c] = np.ones((nA, nA))
gl = goal.lower()
goal_mat = np.ones((nC, nC))


class AHP:
    def __init__(self, alternatives=None, criterias=None, goal=''):
        if criterias is None:
            criterias = []
        if alternatives is None:
            alternatives = []
        self.alternatives = alternatives
        self.criterias = criterias
        self.goal = goal
        self.crit_mat = self._init_crit_matrix()
        self.goal_mat = self._init_goal_matrix()

    def _init_crit_matrix(self):
        nA = len(self.alternatives)
        crit_mat = {}
        for c in crits:
            crit_mat[c] = np.ones((nA, nA))
        return crit_mat

    def _init_goal_matrix(self):
        nC = len(self.criterias)
        return np.ones((nC, nC))

    def _priority_vec(self, M):
        """"
        Priority vectors are obtained:
        * In exact form by raising the matrix to large powers and summing
          each row and dividing each by the total sum of all the rows, OR
        * Approximately by adding each row of the matrix and dividing by
          their total
        """
        w, v = LA.eig(M)
        max_w = np.argmax(w)
        # How `max_w` works: Take all indices of M along the first axis,
        #  but only index max_w along the second
        p_eig = v[:, max_w]
        # Return normalised principal eigenvector
        return np.real(p_eig / np.sum(p_eig))

    def _title(self, title, u="-"):
        print(f" {title} ".center(60, u))

    def _frac_input(self, prompt, hint=""):
        frac = float(0.0)
        valid = False
        while not valid:
            try:
                print(hint) if hint else None
                frac = float(Fraction(input(prompt)))
                valid = True
            except ValueError:
                print("Enter a valid fraction.")
        return frac

    def best_decision(self):
        crits = self.criterias
        alts = self.alternatives
        goal = self.goal
        crit_mat = self.crit_mat
        goal_mat = self.goal_mat

        self._title(goal, u="=")
        gl = goal.lower()
        print()
        # Judgement matrix
        # ----------------
        # (i, j) represents how many more times i is important than j
        # note: if (i, j) = m; then (j, i) = 1/m

        # Prioritise Alts w.r.t Criteria
        for h, c in enumerate(crits):
            cu = c.upper()
            remaining = sum([(nC - h) * nA, (nA * nC) // 2])
            self._title(f"{cu} ({remaining} qs left)")
            mat = crit_mat[c]
            for i, a1 in enumerate(alts):
                for j, a2 in enumerate(alts):
                    if a1 == a2:
                        break
                    # prompt = f"{a2} has better {cu} than {a1} by how times? "
                    prompt = f"When it comes to {cu}, \n" + f"{a2} is ____x better than {a1}?\n"
                    hint = f"Type in a number between 1 to 10 or press s to swap"
                    a_val = self._frac_input(prompt=prompt, hint=hint)
                    mat[i, j] = 1 / a_val
                    mat[j, i] = a_val / 1
            print()

        # Prioritise Criteria w.r.t Goal
        self._title(f"Prioritise criteria ({(nA * nC) // 2} qs left)")
        for i, c1 in enumerate(crits):
            for j, c2 in enumerate(crits):
                c1u, c2u = c1.upper(), c2.upper()
                if c1 == c2:
                    break
                prompt = f"How many times is {c2u} more important to {gl} than {c1u}? "
                c_val = self._frac_input(prompt)
                goal_mat[i, j] = 1 / c_val
                goal_mat[j, i] = c_val / 1

        all_crits_p = np.array([self._priority_vec(p) for p in crit_mat.values()])
        goal_p = self._priority_vec(goal_mat)
        res = np.sum(goal_p * all_crits_p.T, axis=1)
        print()
        self._title("Results", u="#")
        return alts[np.argmax(res)]
