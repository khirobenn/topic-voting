import sys
import pandas as pd
import numpy as np
import pulp as p

nb_etudiants = 25 # Le nombre d'étudiants dans la classe
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

sheet_name = sys.argv[1] # Le nom du fichier excel
sheet_id = sys.argv[2]  # l'id du fichier
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# x sera les données collectées des étudiants
df = pd.read_csv(sheet_url)

# Ici, on vérifie que tout les jetons sont utilisés
nb_jetons = df["Nombre de Jetons restants"]
if nb_jetons.sum() != 0:
    print("Il reste des jetons à utiliser")
    exit()

# On enlève le nom prénom et le nombre de jetons restants pour récupérer que les coefficients
x = df.drop(["First name", "Last name", "Nombre de Jetons restants"], axis=1)
# On met nos données comme un seul vecteur de (nb_etudiants * nb_sujets)
x = np.array(x).flatten()

# On vérifie que y'a aucun sujet qui a 0 jeton
if len(x[x == 0]) != 0:
    print("Il y'a un étudiant qui a mis 0 jetons sur un sujet!")
    exit()

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
for i in range(0,  nb_sujets):
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

groups = np.argmax(solution, axis=1)+1
print("Solution: ", solution)

df["Groupe"] = groups

df.to_csv("fichier_groupes.csv", index=False)