from numpy import linalg as LA
from fractions import Fraction
import numpy as np

# Set printing options precision
# np.set_printoptions(precision=5)
# np.set_printoptions(formatter={'float': '{: 0.2f}'.format})

class AHP:
    def __init__(self, alternatives=None, criterias=None, goal=''):
        if criterias is None:
            criterias = []
        if alternatives is None:
            alternatives = []
        self.alternatives = alternatives
        self.criterias = criterias
        self.goal = goal

    def _init_crit_matrix(self):
        nA = len(self.alternatives)
        crit_mat = {}
        for c in range(len(self.criterias)):
            crit_mat[c] = np.ones((nA, nA))
        self.crit_mat = crit_mat

    def _init_goal_matrix(self):
        nC = len(self.criterias)
        self.goal_mat = np.ones((nC, nC))

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
    
    def compare_alternatives_wrt_criteria(self, alternatives, criteria, multiple):
        """
        Prioritise alternatives w.r.t criteria
        --------------------------------------
        When it comes to criteria, how many more 
        times is alternative1 preferred to alternative2?
        """
        i, j = alternatives
        if not hasattr(self, 'crit_mat'):
            self._init_crit_matrix()
        mat = self.crit_mat[criteria]
        mat[i, j] = multiple / 1
        mat[j, i] = 1 / multiple

    def compare_criterias_wrt_goal(self, criterias, multiple):
        """
        Prioritise criteria w.r.t goal
        ------------------------------
        How many more times is criteria1 more important
        to achieve the goal than criteria2?
        """
        i, j = criterias
        if not hasattr(self, 'goal_mat'):
            self._init_goal_matrix()
        goal_mat = self.goal_mat
        goal_mat[i, j] = multiple / 1
        goal_mat[j, i] = 1 / multiple

    def prioritise(self):
        # 1)
        goal = self.goal
        crits = self.criterias
        alts = self.alternatives
        nA = len(self.alternatives)
        nC = len(self.criterias)

        self._title(goal, u="=")
        gl = goal.lower()
        print()
        # Judgement matrix
        # ----------------
        # (i, j) represents how many more times i is important than j
        # note: if (i, j) = m; then (j, i) = 1/m

        # a) Prioritise alternatives w.r.t criteria
        for h, c in enumerate(crits):
            cu = c.upper()
            remaining = ((nC - h) * nA) + ((nA * nC) // 2)
            self._title(f"{cu} ({remaining} qs left)")
            # mat = crit_mat[c]
            for i, a1 in enumerate(alts):
                for j, a2 in enumerate(alts):
                    if a1 == a2:
                        break
                    prompt = f"When it comes to {cu}, \n" + f"{a2} is ____x better than {a1}?\n"
                    hint = f"Type in a number between 1 to 10 or press s to swap.\n"
                    m = self._frac_input(prompt, hint)
                    self.compare_alternatives_wrt_criteria((i, j), c, m)
            print()

        # b) Prioritise criteria w.r.t goal
        self._title(f"Prioritise criteria ({(nA * nC) // 2} qs left)")
        for i, c1 in enumerate(crits):
            for j, c2 in enumerate(crits):
                c1u, c2u = c1.upper(), c2.upper()
                if c1u == c2u:
                    break
                prompt = f"How many times is {c2u} more important to {gl} than {c1u}? "
                m = self._frac_input(prompt)
                self.compare_criterias_wrt_goal((i, j), m)

    def decide(self):
        # 2) Decide
        if not hasattr(self, 'crit_mat'):
            raise PrioritizationError("Please call prioritize() to prioritise your alternatives with respect to the criteria")
        if not hasattr(self, 'goal_mat'):
            raise PrioritizationError("Please call prioritize() to prioritise your criterias with respect to the goal")
        
        crit_mat = self.crit_mat
        goal_mat = self.goal_mat
        
        all_crits_p = np.array([self._priority_vec(p) for p in crit_mat.values()])
        goal_p = self._priority_vec(goal_mat)
        res = np.sum(goal_p * all_crits_p.T, axis=1)
        
        print()
        self._title("Results", u="#")
        return np.argmax(res)


class PrioritizationError(Exception):
    pass
