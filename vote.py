import numpy as np
import pulp as p

nb_etudiants = 26
nb_sujets = 5

produit = nb_etudiants*nb_sujets

problem = p.LpProblem('objective_function', p.LpMaximize)

# mes variables y :
Y = []
for i in range(0, produit):
    Y.append(p.LpVariable('y'+str(i+1), lowBound=0, upBound=1, cat='Integer'))

x = np.random.rand(produit) * 10
x = x.astype(int) + 1

problem += (x*Y).sum()

for i in range(0, nb_etudiants):
    contrainst = -1
    for j in range(0, nb_sujets):
        contrainst = contrainst + Y[i*5 + j]
    problem += contrainst == 0

k = 0
for i in range(0,  nb_sujets):
    contrainst = 0
    if i == k:
        contrainst = -6
    else:
        contrainst = -5

    for j in range(0, nb_etudiants):
        contrainst = contrainst + Y[j*5 + i]
    problem += contrainst == 0

status = problem.solve()
print(p.LpStatus[status])

solution = []

for i in range(0, nb_etudiants):
    tmp = []
    for j in range(0, nb_sujets):
        tmp.append(p.value(Y[i*5 + j]))
    solution.append(tmp)

solution = np.array(solution)
print(solution)
print(solution.sum(axis=0))
print(solution.sum(axis=1))
