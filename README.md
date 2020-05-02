# Analytical Hiearchy Process

or, decide things more analytically.

This project involves implementing the analytical hierarchy process (AHP) for making tough decisions as mentioned in the 1987 paper, *'The Analytic Process - What it is and how it is used'* by [Thomas L. Saaty](https://en.wikipedia.org/wiki/Thomas_L._Saaty).

AHP defines a framework to evaluate decisions with 3 required things:

1. **Goal** (e.g. 'What fast-food restaurant should we eat at?')
2. **Criteria** (e.g. Distance, cuisine, price etc.)
3. **Alternatives** to pick from (e.g. Pizza Hut, Domino's, Taco Bell).

The first set of questions compare alternatives against the criteria. For example, 'How many more times is Pizza Hut better at price than Domino's?'. An answer of 4 means Pizza Hut is 4 times better at price than Domino's, whereas an answer of 1/4 means Pizza Hut is 1/4 better at price than Domino's (i.e. Domino's is 4 times better).

The second set of questions compare criteria against each other to define the weights of  the judgement matrix. For example, a typical question at this stage would be along the lines of, 'By how many more times is *price* more important than *distance*?'. An answer of 6 means *price* is 6 times more important than *distance*. An answer of 1/8 means *distance* is actually 8 times more important than *price* (reciprocal) - as in the first set of questions.

Finally, the principal eigenvector is computed to modify the weightingo of the alternatives and is used to find the index of the list of alternatives which has the highest weight to pick as a final result.

## Example run-through

Define your goal, criteria and alternatives in `ahp.py` file before running.

```plain
$ python ahp.py

=================== Picking where to eat ===================

------------------- DISTANCE (5 qs left) -------------------
Pizza Hut has better DISTANCE than Dominos by how times? 1/3

-------------------- PRICE (4 qs left) ---------------------
Pizza Hut has better PRICE than Dominos by how times? 1/5

------------------- CUISINE (3 qs left) --------------------
Pizza Hut has better CUISINE than Dominos by how times? 5

------------- Prioritise criteria (3 qs left) --------------
How many times is DISTANCE better at picking where to eat than PRICE? 2
How many times is DISTANCE better at picking where to eat than CUISINE? 1/4
How many times is PRICE better at picking where to eat than CUISINE? 5

========================= Results =========================

Best decision: Dominos
```

---

### Todo

- Don't ask for input, open up an method in the library to allow manual setting of choices
  - It might not be the case that everyone will want to use my input method to do the comparisons
- Heavy dependecy on numpy to compute the eigenvectors, are there any lightweight alternatives?
- Is it possible to separate the modules out? <-- in progress!
