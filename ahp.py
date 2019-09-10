from fractions import Fraction
from numpy import linalg as LA
import numpy as np
import scipy
import math

# Set printing options precision
# np.set_printoptions(precision=5)
# np.set_printoptions(formatter={'float': '{: 0.2f}'.format})

# Define names
alts = ['Guzman', 'Pizza Hut', "Domino's"]
crits = ['Distance', 'Price', 'Cuisine']
goal = 'Picking where to eat'

# Init setup
nA, nC = len(alts), len(crits)
crit_mat = {}
for c in crits:	
	crit_mat[c] = np.ones((nA, nA))
gl = goal.lower()
goal_mat = np.ones((nC, nC))


def p_vec(M):
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
	p_eig = v[:,max_w]
	# Return normalised principal eigenvector
	return np.real(p_eig/np.sum(p_eig))

def title(title, u="-"):
	print(f" {title} ".center(60, u))

def frac_input(prompt):
	frac = float(0.0)
	valid = False
	while not valid:
		try:
			frac = float(Fraction(input(prompt)))
			valid = True
		except ValueError:
			print("Enter a valid fraction.")
	return frac


title(goal, u="=")
print()

# Judgement matrix
# ----------------
# (i, j) represents how many more times i is important than j
# note: if (i, j) = m; then (j, i) = 1/m

# Prioritise Alts w.r.t Criteria
for h, c in enumerate(crits):
	cu = c.upper()
	remaining = sum([(nC - h) * nA, (nA * nC) // 2])
	title(f"{cu} ({remaining} qs left)")
	mat = crit_mat[c]
	for i, a1 in enumerate(alts):
		for j, a2 in enumerate(alts):
			if a1 == a2:
				break
			prompt = f"{a2} has better {cu} than {a1} by how times? "
			a_val = frac_input(prompt)
			mat[i, j] = 1 / a_val
			mat[j, i] = a_val / 1
	print()

# Prioritise Criteria w.r.t Goal
title(f"Prioritise criteria ({(nA * nC) // 2} qs left)")
for i, c1 in enumerate(crits):
	for j, c2 in enumerate(crits):
		c1u, c2u = c1.upper(), c2.upper()
		if c1 == c2:
			break
		prompt = f"How many times is {c2u} better at {gl} than {c1u}? "
		c_val = frac_input(prompt)
		goal_mat[i, j] = 1 / c_val
		goal_mat[j, i] = c_val / 1

all_crits_p = np.array([p_vec(p) for p in crit_mat.values()])
goal_p = p_vec(goal_mat)
res = np.sum(goal_p * all_crits_p.T, axis=1)

print()
title("Results", u="#")
print(alts[np.argmax(res)])