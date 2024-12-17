import networkx as nx
import matplotlib.pyplot as plt

# Création du graphe
G = nx.DiGraph()
# Ajout des nœuds représentant les règles
rules = [f"Règle {i}" for i in range(1, 11)]
G.add_nodes_from(rules)
# Ajout des relations entre les règles sous forme d'arêtes
edges = [
    ("Règle 1", "Règle 8"),
    ("Règle 2", "Règle 8"),
    ("Règle 3", "Règle 8"),
    ("Règle 4", "Règle 8"),
    ("Règle 5", "Règle 8"),
    ("Règle 6", "Règle 8"),
    ("Règle 7", "Règle 8"),
    ("Règle 8", "Règle 9"),
    ("Règle 8", "Règle 10"),
    ("Règle 3", "Règle 10")
]
G.add_edges_from(edges)
# Dessin du graphe
plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G, seed=42)  # Positionnement des nœuds
nx.draw(
    G, pos, with_labels=True, node_size=3000, node_color="lightblue",
    font_size=10, font_weight="bold", edge_color="gray", arrowsize=20
)
# Affichage
plt.title("Relations entre les règles", fontsize=14)
plt.show()

import networkx as nx
import matplotlib.pyplot as plt

# Définir les règles sous forme de graphes orientés (prémisse → conclusion)
rules = [
    ("Fièvre", "Isoler le travailleur"),
    ("Toux", "Isoler le travailleur"),
    ("Difficulté à respirer", "Isoler le travailleur"),
    ("Perte de l’odorat", "Isoler le travailleur"),
    (("Fatigue", "Mal de ventre"), "Isoler le travailleur"),
    (("Fatigue", "Nez bouché"), "Isoler le travailleur"),
    (("Mal de ventre", "Nez bouché"), "Isoler le travailleur"),
    ("Isoler le travailleur", "Téléphoner"),
    (("Isoler le travailleur", "Téléphoner"), "Identifier les contacts"),
    (("Isoler le travailleur", "Difficulté à respirer"), "Téléphoner"),
]

# Créer un graphe dirigé
graph = nx.DiGraph()

# Ajouter les règles au graphe
for rule in rules:
    if isinstance(rule[0], tuple):  # Si la prémisse est multiple
        for prem in rule[0]:
            graph.add_edge(prem, rule[1])
    else:
        graph.add_edge(rule[0], rule[1])

# Calculer un ordre topologique (priorité des règles)
try:
    execution_order = list(nx.topological_sort(graph))
    print("Ordre d'exécution des règles :", execution_order)
except nx.NetworkXUnfeasible:
    print("Erreur : Les règles contiennent des dépendances circulaires.")

# Visualisation du graphe
plt.figure(figsize=(10, 6))
nx.draw(graph, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight="bold", arrowsize=20)
plt.title("Ordre d'exécution des règles")
plt.show()

import networkx as nx
import matplotlib.pyplot as plt

# Définir les règles sous forme de graphes orientés (prémisse → conclusion)
rules = [
    ("Fièvre", "Isoler le travailleur"),
    ("Toux", "Isoler le travailleur"),
    ("Difficulté à respirer", "Isoler le travailleur"),
    ("Perte de l’odorat", "Isoler le travailleur"),
    (("Fatigue", "Mal de ventre"), "Isoler le travailleur"),
    (("Fatigue", "Nez bouché"), "Isoler le travailleur"),
    (("Mal de ventre", "Nez bouché"), "Isoler le travailleur"),
    ("Isoler le travailleur", "Téléphoner"),
    (("Isoler le travailleur", "Téléphoner"), "Identifier les contacts"),
    (("Isoler le travailleur", "Difficulté à respirer"), "Téléphoner"),
]
# Créer un graphe dirigé
graph = nx.DiGraph()
# Ajouter les règles au graphe
for rule in rules:
    if isinstance(rule[0], tuple):  # Si la prémisse est multiple
        for prem in rule[0]:
            graph.add_edge(prem, rule[1])
    else:
        graph.add_edge(rule[0], rule[1])

# Calculer un ordre topologique (priorité des règles)
try:
    execution_order = list(nx.topological_sort(graph))
    print("Ordre d'exécution des règles :", execution_order)
except nx.NetworkXUnfeasible:
    print("Erreur : Les règles contiennent des dépendances circulaires.")

# Visualisation du graphe
plt.figure(figsize=(10, 6))
nx.draw(graph, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight="bold", arrowsize=20)
plt.title("Ordre d'exécution des règles")
plt.show()

# Règles du système (prémisses → conclusion)
rules = [
    {"if": ["Fièvre"], "then": "Isoler le travailleur"},
    {"if": ["Toux"], "then": "Isoler le travailleur"},
    {"if": ["Difficulté à respirer"], "then": "Isoler le travailleur"},
    {"if": ["Perte de l’odorat"], "then": "Isoler le travailleur"},
    {"if": ["Fatigue", "Mal de ventre"], "then": "Isoler le travailleur"},
    {"if": ["Fatigue", "Nez bouché"], "then": "Isoler le travailleur"},
    {"if": ["Mal de ventre", "Nez bouché"], "then": "Isoler le travailleur"},
    {"if": ["Isoler le travailleur"], "then": "Téléphoner"},
    {"if": ["Isoler le travailleur", "Téléphoner"], "then": "Identifier les contacts"},
    {"if": ["Isoler le travailleur", "Difficulté à respirer"], "then": "Téléphoner"},
]
# Base de faits initiale
facts = {"Fièvre"}


# Fonction pour vérifier si une règle est applicable
def is_applicable(rule, known_facts):
    return all(condition in known_facts for condition in rule["if"])


# Fonction de chaînage avant
def forward_chaining(rules, initial_facts):
    facts = set(initial_facts)  # Convertir en ensemble pour éviter les doublons
    new_facts = True  # Variable pour suivre les nouvelles déductions
    proven_facts_sequence = []  # Garder une trace des faits prouvés

    while new_facts:
        new_facts = False
        for rule in rules:
            if is_applicable(rule, facts) and rule["then"] not in facts:
                facts.add(rule["then"])
                new_facts = True
                proven_facts_sequence.append(rule["then"])

    return proven_facts_sequence


# Exécution du chaînage avant
proven_facts = forward_chaining(rules, facts)
print("Suite des faits prouvés :", proven_facts)

# Définir la base de faits (initiale)
base_faits = {'Difficulté à respirer'}

# Définir les règles sous forme de dictionnaire (une clé pour la conclusion et une valeur pour les prémisses)
regles = {
    'Contact avec le travailleur symptomatique': {
        'Difficulté à respirer': True,
        'Fièvre': True
    },
    'Symptôme respiratoire': {
        'Difficulté à respirer': True
    },
    'Contact avec le travailleur infecté': {
        'Symptôme respiratoire': True
    }
}


# Fonction de chaînage arrière
def chaine_arriere(fait_initial):
    faits_requis = []
    succes = False

    # Pour chaque règle, on essaie de vérifier si on peut prouver la conclusion à partir des faits
    for conclusion, conditions in regles.items():
        if fait_initial in conditions:
            faits_requis.append((conclusion, True))
            succes = True
        else:
            faits_requis.append((conclusion, False))

    return faits_requis, succes


# Application du chaînage arrière sur le fait initial
fait_initial = 'Difficulté à respirer'

# Appeler la fonction pour prouver le fait
resultat, succes = chaine_arriere(fait_initial)

# Affichage des résultats
if succes:
    print(f"Le chaînage arrière a été un succès, voici les règles essayées :")
    for conclusion, etat in resultat:
        print(f"Règle : {conclusion} - Résultat: {'Succès' if etat else 'Échec'}")
else:
    print("Le chaînage arrière a échoué. Aucun contact symptomatique prouvé.")


# Définir un système expert simple pour simuler le chaînage avant

class ExpertSystem:
    def __init__(self):
        self.facts = set()  # Ensemble pour stocker les faits

    def assert_fact(self, fact):
        """Ajouter un fait à l'ensemble des faits."""
        self.facts.add(fact)
        print(f"Fait ajouté: {fact}")

    def run(self):
        """Exécute les règles du système expert."""
        self.apply_rules()

    def apply_rules(self):
        """Appliquer les règles pour déterminer si le contact avec un travailleur symptomatique est prouvé."""

        # Règle 1: Si on a "Difficulte-a-respirer" et "Fièvre", prouver "Contact-symptomatique"
        if "Difficulte-a-respirer" in self.facts and "Fièvre" in self.facts:
            self.assert_fact("Contact-symptomatique")
            print("Règle 1 appliquée: Le travailleur a été en contact avec un travailleur symptomatique.")

        # Règle 2: Si on a "Difficulte-a-respirer", prouver "Symptome-respiratoire"
        if "Difficulte-a-respirer" in self.facts:
            self.assert_fact("Symptome-respiratoire")
            print("Règle 2 appliquée: Le travailleur présente un symptôme respiratoire.")

        # Règle 3: Si on a "Symptome-respiratoire", prouver "Contact-travailleur-infecte"
        if "Symptome-respiratoire" in self.facts:
            self.assert_fact("Contact-travailleur-infecte")
            print("Règle 3 appliquée: Le travailleur a été en contact avec un travailleur infecté.")

        # Vérifier si le contact avec un travailleur symptomatique est prouvé
        if "Contact-symptomatique" in self.facts:
            print("Le travailleur a été en contact avec un travailleur symptomatique. Succès!")
        else:
            print("Aucun contact avec un travailleur symptomatique trouvé. Échec.")


# Utilisation de l'expert system

# Créer une instance du système expert
expert_system = ExpertSystem()

# Ajouter des faits initiaux
expert_system.assert_fact("Difficulte-a-respirer")  # Le travailleur a des difficultés à respirer

# Ajouter un autre fait pour tester le cas où il y a de la fièvre
expert_system.assert_fact("Fièvre")  # Le travailleur a de la fièvre

# Exécuter le système pour appliquer les règles
expert_system.run()