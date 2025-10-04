import sys
import pandas as pd
import numpy as np
import pulp as p

nb_etudiants = 26 # Le nombre d'étudiants dans la classe
nb_sujets = 5 # Le nombre de sujets proposés
my_solutions = []
my_maximums = []
produit = nb_etudiants*nb_sujets

problem = p.LpProblem('objective_function', p.LpMaximize)

# mes variables y :
# chaque y est un entier £ {0, 1}
Y = []
for i in range(0, produit):
    Y.append(p.LpVariable('y'+str(i+1), lowBound=0, upBound=1, cat='Integer'))

# x sera les données collectées des étudiants
x = pd.read_csv(sys.argv[1])
x = x.drop(["First name", "Last name"], axis=1)
x = np.array(x).flatten()

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
for k in range(0, 5):
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

    # ici, on récupère la solution dans une matrice de (nb_etudiants x nb_sujets)
    solution = []

    
    for i in range(0, nb_etudiants):
        tmp = []
        for j in range(0, nb_sujets):
            tmp.append(p.value(Y[i*5 + j]))
        solution.append(tmp)

    solution = np.array(solution)

    # On stocke la solution pour le k courant
    my_solutions.append(solution)
    # On stocke le résultat de la fonction objective (son maximum) pour le k courant
    my_maximums.append(problem.objective.value())

    # On enlève les contraintes mise sur les colonnes
    # pour les mettre à jour à l'incrémentation du k
    for i in range(0, 5):
        problem.constraints.popitem()


print(my_solutions)
print(my_maximums)

# Notre solution est celle qui donne la plus grande valeurs dans my_maximum
my_sol = my_solutions[np.argmax(my_maximums)]
print("Solution: ", my_sol)