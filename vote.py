import numpy as np
import pulp as p

nb_etudiants = 26 # Le nombre d'étudiants dans la classe
nb_sujets = 5 # Le nombre de sujets proposés

produit = nb_etudiants*nb_sujets

problem = p.LpProblem('objective_function', p.LpMaximize)

# mes variables y :
# chaque y est un entier £ {0, 1}
Y = []
for i in range(0, produit):
    Y.append(p.LpVariable('y'+str(i+1), lowBound=0, upBound=1, cat='Integer'))

# x sera les données collectées des étudiants
x = np.random.rand(produit) * 10
x = x.astype(int) + 1

# la fonction qu'il faut maximiser
problem += (x*Y).sum()

# L'ajout des contraintes sur les lignes
for i in range(0, nb_etudiants):
    contrainst = -1
    for j in range(0, nb_sujets):
        contrainst = contrainst + Y[i*5 + j]
    problem += contrainst == 0

# L'ajout des contraintes sur les colonnes
# le k faut le faire varier après pour obtenir tout les cas possible
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

# Maintenant on résoud le système
status = problem.solve()
print(p.LpStatus[status])


# ici, on récupère la solution
solution = []

for i in range(0, nb_etudiants):
    tmp = []
    for j in range(0, nb_sujets):
        tmp.append(p.value(Y[i*5 + j]))
    solution.append(tmp)

# on affiche la solution et on vérifie si les contraintes sont respectées
solution = np.array(solution)
print(solution)
print(solution.sum(axis=0))
print(solution.sum(axis=1))
