# -*- coding: utf-8 -*-
#"""
#QUIZ KOLIE
#Application de Quiz - Interface professionnelle
#Compatible Pydroid3 (necessite le module Kivy : pip install kivy)

#Ecrans :
# - welcome     : accueil + bouton ENTRER
 - menu        : QUIZ / REVISION / EXAMEN / INFO / PARAMETRES
 - quiz        : questions a choix multiple, sans limite de temps
 - examen_intro: presentation de l'examen avant de commencer
 - examen      : questions a choix multiple, avec minuteur
 - resultat    : ecran de score partage par le quiz et l'examen
 - revision    : fiches question/reponse (flashcards)
 - info        : informations sur l'application + meilleurs scores
 - parametres  : son, difficulte, reinitialisation de la progression
"""

import random

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

# ---------- Palette de couleurs (theme sombre professionnel) ----------
BG_DARK_1 = get_color_from_hex("#0B1220")
BG_DARK_2 = get_color_from_hex("#161E33")
ACCENT = get_color_from_hex("#4C6FFF")
ACCENT_DARK = get_color_from_hex("#2F49C9")
GOLD = get_color_from_hex("#F2B705")
GREEN = get_color_from_hex("#2ECC71")
RED = get_color_from_hex("#E74C3C")
TEXT_LIGHT = get_color_from_hex("#F4F6FB")
TEXT_MUTED = get_color_from_hex("#9AA5C0")
CARD_BG = get_color_from_hex("#1D2740")
CARD_SHADOW = get_color_from_hex("#05070C")


# ============================================================
#  DONNEES DE L'APPLICATION (a remplacer / completer librement)
# ============================================================

QUESTIONS_QUIZ = [
    {"question": "Quelle est la capitale de la France ?",
     "options": ["Lyon", "Marseille", "Paris", "Nice"], "answer": 2},
    {"question": "Combien font 7 x 8 ?",
     "options": ["54", "56", "58", "64"], "answer": 1},
    {"question": "Quel est le plus grand ocean du monde ?",
     "options": ["Atlantique", "Indien", "Arctique", "Pacifique"], "answer": 3},
    {"question": "En quelle annee a eu lieu la Revolution francaise ?",
     "options": ["1789", "1804", "1848", "1918"], "answer": 0},
    {"question": "Quel est le symbole chimique de l'or ?",
     "options": ["Ag", "Au", "Fe", "Pb"], "answer": 1},
]

QUESTIONS_EXAMEN = list(QUESTIONS_QUIZ)  # compatibilite
EXAMEN_DUREE_SEC = 25  # 25 secondes par question
VERSION_RESULTATS = "v2.1 - classement interactif"
QUESTIONS_PAR_MATIERE_EXAMEN = 5
EXAM_USED_INDICES = {}

REVISION_CARDS = [
    {"question": "Quelle est la capitale de la France ?", "answer": "Paris"},
    {"question": "Combien font 7 x 8 ?", "answer": "56"},
    {"question": "Quel est le plus grand ocean du monde ?", "answer": "Pacifique"},
    {"question": "En quelle annee a eu lieu la Revolution francaise ?", "answer": "1789"},
    {"question": "Quel est le symbole chimique de l'or ?", "answer": "Au (Or)"},
]

APP_SETTINGS = {"son": True, "difficulte": "Intermediaire"}
BEST_SCORES = {"quiz": 0, "examen": 0}

# -----------------------------------------------------------------
# RESULTATS D EXAMEN : candidats IA et publication des classements
# Les candidats sont des personnages simulés par l application.
# 50 candidats école, 400 région, 1500 national.
# -----------------------------------------------------------------
IA_PRENOMS = [
    "Mamadou", "Ibrahima", "Alpha", "Mohamed", "Abdoulaye", "Oumar",
    "Amadou", "Sékou", "Boubacar", "Youssouf", "Lansana", "Fodé",
    "Moussa", "Thierno", "Abdoul", "Karim", "Ismaël", "Souleymane",
    "Mory", "Karamoko", "Aïssatou", "Fatoumata", "Mariama", "Aminata",
    "Hawa", "Kadiatou", "Binta", "Mariam", "Aïcha", "Fanta",
    "Hindou", "Adama", "Nana", "Saran", "Maimouna", "Sia", "Néné",
    "Kadi", "Safiatou", "Ramatoulaye", "Nafissatou", "Hadja", "Aminata",
    "Salimatou", "Awa", "Béatrice", "Justine", "Angeline", "Caroline", "Denise"
]
IA_NOMS = [
    "Diallo", "Camara", "Condé", "Sylla", "Kourouma", "Bangoura", "Soumah",
    "Touré", "Keita", "Conté", "Diarra", "Kaba", "Cissé", "Fofana",
    "Sow", "Bah", "Barry", "Baldé", "Tolno", "Kolié", "Gbanamou",
    "Koïvogui", "Koïlamy", "Gamy", "Goumoû", "Tambassa", "Zoumanigui",
    "Sâa", "Bilivogui", "Komano", "Borgo", "Lamarana", "Sadjo", "Traoré",
    "Coulibaly", "Camara", "Diallo", "Condé", "Kourouma", "Bangoura"
]

IA_CANDIDATE_NAMES = [
    "{} {}".format(prenom, nom)
    for prenom in IA_PRENOMS for nom in IA_NOMS
]
# Retire les doublons tout en conservant l ordre.
IA_CANDIDATE_NAMES = list(dict.fromkeys(IA_CANDIDATE_NAMES))
IA_COUNTS = {"ecole": 50, "regional": 400, "national": 1500}
IA_AGENTS_CORRECTION = [
    ("Mariam Kourouma", "IA - correction des copies"),
    ("Ibrahima Diallo", "IA - vérification des réponses"),
    ("Aïssatou Camara", "IA - classement et publication"),
]
LAST_EXAM_RESULT = {}

# Niveaux scolaires disponibles dans l'onglet QUIZ
NIVEAUX_PRIMAIRE = ["1ere A", "2eme A", "3eme A", "4eme A", "5eme A", "6eme A"]
NIVEAUX_COLLEGE = ["7eme A", "8eme A", "9eme A", "10eme A"]
NIVEAUX_LYCEE = ["11eme A", "12eme A", "Terminale A"]
SERIES_LYCEE = ["SM", "SS", "SE"]

# Matieres par categorie de niveau
PRIMAIRE_MATIERES = ["Francais", "Geographie", "Histoire", "E.C.M", "Sciences d'observation", "Maths"]
COLLEGE_MATIERES = ["Francais", "Maths", "Histoire", "Geographie", "E.C.M", "Biologie", "Anglais", "Physique et Chimie"]
LYCEE_SM_SE_MATIERES = ["Maths", "Physique", "Chimie", "Francais", "Economie", "Biologie", "Philosophie", "Geologie"]
LYCEE_SS_MATIERES = ["Francais", "Anglais", "Philosophie", "Histoire", "Geographie", "Economie"]

QUESTIONS_PAR_QUIZ = 20

# Banque de questions : cle = (niveau, matiere) -> liste de questions.
# Chaque matiere devrait idealement contenir plusieurs centaines de questions ;
# seules quelques matieres sont pre-remplies ici a titre d'exemple/demo.
QUESTION_BANKS = {}

# Suivi des questions deja posees par (niveau, matiere), pour que le prochain
# quiz propose un lot different tant que la banque n'est pas epuisee.
USED_INDICES = {}


def get_questions(niveau, matiere, n=QUESTIONS_PAR_QUIZ):
    """Renvoie n questions non deja posees pour ce (niveau, matiere).
    Quand toutes les questions de la banque ont ete utilisees, le cycle
    recommence depuis le debut (rotation complete)."""
    key = (niveau, matiere)
    bank = QUESTION_BANKS.get(key)
    if not bank:
        return []
    used = USED_INDICES.setdefault(key, set())
    available = [i for i in range(len(bank)) if i not in used]
    if len(available) < n:
        used.clear()
        available = list(range(len(bank)))
    chosen = random.sample(available, min(n, len(available)))
    used.update(chosen)
    return [bank[i] for i in chosen]


# ---- Exemples de banques (a completer / remplacer par du vrai contenu) ----

QUESTION_BANKS[("1ere A", "Maths")] = [
    {"question": "Combien font 2 + 3 ?", "options": ["4", "5", "6", "7"], "answer": 1},
    {"question": "Combien font 5 + 4 ?", "options": ["8", "9", "10", "7"], "answer": 1},
    {"question": "Combien font 7 - 2 ?", "options": ["4", "5", "6", "3"], "answer": 1},
    {"question": "Combien font 9 - 3 ?", "options": ["5", "6", "7", "4"], "answer": 1},
    {"question": "Combien font 4 + 4 ?", "options": ["6", "7", "8", "9"], "answer": 2},
    {"question": "Combien font 10 - 5 ?", "options": ["3", "4", "5", "6"], "answer": 2},
    {"question": "Combien font 6 + 3 ?", "options": ["8", "9", "10", "7"], "answer": 1},
    {"question": "Combien font 8 - 4 ?", "options": ["2", "3", "4", "5"], "answer": 2},
    {"question": "Quel nombre vient apres 12 ?", "options": ["11", "13", "14", "10"], "answer": 1},
    {"question": "Quel nombre vient avant 9 ?", "options": ["7", "8", "10", "6"], "answer": 1},
    {"question": "Combien font 3 + 6 ?", "options": ["7", "8", "9", "10"], "answer": 2},
    {"question": "Combien font 10 - 6 ?", "options": ["2", "3", "4", "5"], "answer": 2},
    {"question": "Combien font 5 + 5 ?", "options": ["9", "10", "11", "8"], "answer": 1},
    {"question": "Combien font 2 + 7 ?", "options": ["8", "9", "10", "7"], "answer": 1},
    {"question": "Combien y a-t-il de jours dans une semaine ?", "options": ["5", "6", "7", "8"], "answer": 2},
    {"question": "Quelle forme a 3 cotes ?", "options": ["Carre", "Triangle", "Cercle", "Rectangle"], "answer": 1},
    {"question": "Quelle forme a 4 cotes egaux ?", "options": ["Triangle", "Cercle", "Carre", "Losange"], "answer": 2},
    {"question": "Combien font 6 - 1 ?", "options": ["4", "5", "6", "3"], "answer": 1},
    {"question": "Combien font 1 + 8 ?", "options": ["7", "8", "9", "10"], "answer": 2},
    {"question": "Combien font 9 + 1 ?", "options": ["9", "10", "11", "8"], "answer": 1},
    {"question": "Quel nombre est plus grand : 8 ou 6 ?", "options": ["6", "8", "Ils sont egaux", "Aucun"], "answer": 1},
    {"question": "Combien font 4 + 5 ?", "options": ["8", "9", "10", "7"], "answer": 1},
    {"question": "Combien font 7 + 2 ?", "options": ["8", "9", "10", "7"], "answer": 1},
    {"question": "Combien font 10 - 3 ?", "options": ["6", "7", "8", "5"], "answer": 1},
]

QUESTION_BANKS[("10eme A", "Maths")] = [
    {"question": "Quelle est la valeur de x dans 2x + 3 = 11 ?", "options": ["3", "4", "5", "6"], "answer": 1},
    {"question": "Combien font 3/4 en pourcentage ?", "options": ["70%", "75%", "80%", "60%"], "answer": 1},
    {"question": "Quelle est l'aire d'un carre de cote 6 cm ?", "options": ["12 cm2", "24 cm2", "36 cm2", "30 cm2"], "answer": 2},
    {"question": "Quel est le perimetre d'un rectangle de 5 cm sur 3 cm ?", "options": ["8 cm", "15 cm", "16 cm", "18 cm"], "answer": 2},
    {"question": "Simplifie la fraction 8/12.", "options": ["2/3", "3/4", "4/6", "1/2"], "answer": 0},
    {"question": "Quelle est la racine carree de 81 ?", "options": ["7", "8", "9", "10"], "answer": 2},
    {"question": "Dans un triangle rectangle, comment s'appelle le plus grand cote ?", "options": ["Cathete", "Hypotenuse", "Mediane", "Base"], "answer": 1},
    {"question": "Combien font 15% de 200 ?", "options": ["20", "25", "30", "35"], "answer": 2},
    {"question": "Resous : 5x = 45.", "options": ["x=8", "x=9", "x=10", "x=7"], "answer": 1},
    {"question": "Quelle est la somme des angles d'un triangle ?", "options": ["90 degres", "180 degres", "270 degres", "360 degres"], "answer": 1},
    {"question": "Quel est le PGCD de 12 et 18 ?", "options": ["3", "4", "6", "9"], "answer": 2},
    {"question": "Quel est le PPCM de 4 et 6 ?", "options": ["8", "10", "12", "24"], "answer": 2},
    {"question": "Combien font (-3) x 4 ?", "options": ["-12", "12", "-7", "7"], "answer": 0},
    {"question": "Developpe : 3(x + 2).", "options": ["3x+2", "3x+6", "x+6", "3x+5"], "answer": 1},
    {"question": "Quelle est la valeur de pi arrondie a 2 decimales ?", "options": ["3.14", "3.41", "3.12", "3.16"], "answer": 0},
    {"question": "Un angle de 90 degres est appele...", "options": ["Aigu", "Obtus", "Droit", "Plat"], "answer": 2},
    {"question": "Combien font 2^5 ?", "options": ["10", "16", "32", "25"], "answer": 2},
    {"question": "Quelle est la moyenne de 4, 6 et 8 ?", "options": ["5", "6", "7", "8"], "answer": 1},
    {"question": "Resous : x - 7 = 3.", "options": ["x=9", "x=10", "x=11", "x=8"], "answer": 1},
    {"question": "Combien de faces a un cube ?", "options": ["4", "6", "8", "12"], "answer": 1},
    {"question": "Quel est l'oppose de -5 ?", "options": ["5", "-5", "0", "10"], "answer": 0},
    {"question": "Combien font 7/10 en decimal ?", "options": ["0.07", "0.7", "7.0", "0.007"], "answer": 1},
    {"question": "Le volume d'un cube de cote 3 cm est :", "options": ["9 cm3", "18 cm3", "27 cm3", "24 cm3"], "answer": 2},
    {"question": "Resous : 4x - 1 = 11.", "options": ["x=2", "x=3", "x=4", "x=5"], "answer": 1},
]

QUESTION_BANKS[("Terminale A (SM)", "Maths")] = [
    {"question": "Quelle est la derivee de x^2 ?", "options": ["x", "2x", "x^2", "2"], "answer": 1},
    {"question": "Quelle est la derivee de sin(x) ?", "options": ["cos(x)", "-cos(x)", "-sin(x)", "tan(x)"], "answer": 0},
    {"question": "La limite de 1/x quand x tend vers +infini est :", "options": ["+infini", "0", "1", "-infini"], "answer": 1},
    {"question": "Quelle est la primitive de 2x ?", "options": ["x^2", "x^2 + C", "2x^2", "x"], "answer": 1},
    {"question": "ln(1) est egal a :", "options": ["0", "1", "e", "Indefini"], "answer": 0},
    {"question": "e^0 est egal a :", "options": ["0", "1", "e", "Indefini"], "answer": 1},
    {"question": "Quelle est la derivee de e^x ?", "options": ["e^x", "x*e^x", "1", "e"], "answer": 0},
    {"question": "Un nombre complexe s'ecrit sous la forme :", "options": ["a + bi", "a - b", "a * b", "a / b"], "answer": 0},
    {"question": "Le module de i est :", "options": ["0", "1", "-1", "i"], "answer": 1},
    {"question": "La derivee d'une constante est :", "options": ["1", "0", "la constante", "indefinie"], "answer": 1},
    {"question": "Quelle est la solution de x^2 = 4 ?", "options": ["x=2 uniquement", "x=-2 uniquement", "x=2 ou x=-2", "Aucune solution"], "answer": 2},
    {"question": "Le discriminant delta = b^2 - 4ac permet de trouver :", "options": ["La derivee", "Les racines d'une equation du 2e degre", "L'integrale", "La limite"], "answer": 1},
    {"question": "Une fonction est croissante quand sa derivee est :", "options": ["Negative", "Positive", "Nulle", "Indefinie"], "answer": 1},
    {"question": "Quelle est l'integrale de 1 sur [0,1] ?", "options": ["0", "1", "2", "0.5"], "answer": 1},
    {"question": "log(100) en base 10 est egal a :", "options": ["1", "2", "10", "100"], "answer": 1},
    {"question": "La probabilite d'un evenement est toujours comprise entre :", "options": ["-1 et 1", "0 et 1", "0 et 100", "1 et 10"], "answer": 1},
    {"question": "Deux evenements incompatibles ont une intersection :", "options": ["Egale a 1", "Vide", "Egale a l'univers", "Indefinie"], "answer": 1},
    {"question": "La derivee de 1/x est :", "options": ["-1/x^2", "1/x^2", "ln(x)", "-x"], "answer": 0},
    {"question": "Une suite geometrique de raison q converge si :", "options": ["q > 1", "|q| < 1", "q = 0", "q < -1"], "answer": 1},
    {"question": "cos(0) est egal a :", "options": ["0", "1", "-1", "0.5"], "answer": 1},
    {"question": "sin(pi/2) est egal a :", "options": ["0", "1", "-1", "0.5"], "answer": 1},
    {"question": "La derivee de ln(x) est :", "options": ["1/x", "x", "ln(x)", "1"], "answer": 0},
    {"question": "Un vecteur nul a pour norme :", "options": ["1", "0", "-1", "Indefinie"], "answer": 1},
    {"question": "La matrice identite d'ordre 2 a pour determinant :", "options": ["0", "1", "2", "4"], "answer": 1},
]



# -----------------------------------------------------------------
# MOTEUR DE L EXAMEN MULTIMATIERE
# 5 questions par matiere, toutes les matieres de la classe.
# Les questions d examen utilisent un suivi independant de celui du Quiz.
# -----------------------------------------------------------------
def get_exam_questions(niveau, matieres, n_par_matiere=QUESTIONS_PAR_MATIERE_EXAMEN):
    result = []
    for matiere in matieres:
        bank = QUESTION_BANKS.get((niveau, matiere), [])
        if not bank:
            continue
        key = (niveau, matiere)
        used = EXAM_USED_INDICES.setdefault(key, set())
        available = [i for i in range(len(bank)) if i not in used]
        if len(available) < n_par_matiere:
            # Nouveau cycle pour cette matiere quand la banque est epuisee.
            used.clear()
            available = list(range(len(bank)))
        random.shuffle(available)
        selected = available[:min(n_par_matiere, len(available))]
        used.update(selected)
        for idx in selected:
            q = dict(bank[idx])
            q["matiere"] = matiere
            result.append(q)
    random.shuffle(result)
    return result


# -----------------------------------------------------------------
# BANQUES COMPLETES DU QUIZ
# Chaque matiere dispose d'au moins 20 questions independantes.
# Le moteur tire exactement QUESTIONS_PAR_QUIZ questions dans la banque
# de la matiere choisie. Les banques existantes ci-dessus restent prioritaires.
# -----------------------------------------------------------------
def _bank(items):
    return [{"question": q, "options": list(opts), "answer": a} for q, opts, a in items]

QUESTION_BANKS_MATIERES = {}

QUESTION_BANKS_MATIERES["Francais"] = _bank([
    ("Quel est le contraire de 'rapide' ?", ("Lent", "Vif", "Prompt", "Agile"), 0),
    ("Dans 'Les enfants jouent', quel est le sujet ?", ("jouent", "Les enfants", "enfants jouent", "Les"), 1),
    ("Quel mot est un verbe ?", ("Maison", "Courir", "Bleu", "Rapidement"), 1),
    ("Quel est le pluriel de 'cheval' ?", ("Chevals", "Chevaux", "Chevales", "Chevaus"), 1),
    ("Quel est le féminin de 'acteur' ?", ("Actrice", "Acteuse", "Acteure", "Acteurie"), 0),
    ("Dans 'une belle maison', quel mot est un adjectif ?", ("une", "belle", "maison", "dans"), 1),
    ("Quel signe termine normalement une question ?", (".", "!", "?", ":"), 2),
    ("Quel est un synonyme de 'heureux' ?", ("Triste", "Content", "Fache", "Fatigue"), 1),
    ("Quel est l'antonyme de 'facile' ?", ("Simple", "Aise", "Difficile", "Possible"), 2),
    ("Dans 'Je mange une pomme', quel est le COD ?", ("Je", "mange", "une pomme", "une"), 2),
    ("Quel temps est 'je partirai' ?", ("Present", "Imparfait", "Futur simple", "Passe compose"), 2),
    ("Quel temps est 'nous avons fini' ?", ("Passe compose", "Futur", "Imparfait", "Present"), 0),
    ("Quel mot est un adverbe ?", ("Doucement", "Maison", "Chanter", "Heureux"), 0),
    ("Quel est le genre du nom 'table' ?", ("Masculin", "Feminin", "Neutre", "Pluriel"), 1),
    ("Quel est le pluriel de 'journal' ?", ("Journals", "Journaux", "Journalx", "Journales"), 1),
    ("Dans 'Paul et Marie arrivent', quel est le verbe ?", ("Paul", "Marie", "et", "arrivent"), 3),
    ("Quel mot contient un prefixe ?", ("Impossible", "Table", "Livre", "Pomme"), 0),
    ("Quel est le contraire de 'commencer' ?", ("Debuter", "Continuer", "Terminer", "Entrer"), 2),
    ("Une phrase qui donne un ordre est une phrase...", ("Declarative", "Interrogative", "Imperative", "Exclamative"), 2),
    ("Quel est le role principal d'un dictionnaire ?", ("Mesurer", "Definir les mots", "Calculer", "Dessiner"), 1),
])

QUESTION_BANKS_MATIERES["Maths"] = _bank([
    ("Combien font 12 + 8 ?", ("18", "20", "22", "24"), 1),
    ("Combien font 15 - 7 ?", ("6", "7", "8", "9"), 2),
    ("Combien font 6 x 7 ?", ("36", "42", "48", "49"), 1),
    ("Combien font 72 / 8 ?", ("8", "9", "10", "12"), 1),
    ("Quelle est la moitie de 50 ?", ("20", "25", "30", "35"), 1),
    ("Quel est le quart de 100 ?", ("20", "25", "30", "40"), 1),
    ("Combien font 3/4 en decimal ?", ("0,25", "0,5", "0,75", "1,25"), 2),
    ("Combien font 25% de 200 ?", ("25", "40", "50", "75"), 2),
    ("Quel est le carre de 9 ?", ("18", "27", "72", "81"), 3),
    ("Quelle est la racine carree de 64 ?", ("6", "7", "8", "9"), 2),
    ("Combien de cotes a un triangle ?", ("2", "3", "4", "5"), 1),
    ("Combien de sommets a un carre ?", ("3", "4", "5", "6"), 1),
    ("Quelle est la somme des angles d'un triangle ?", ("90 degres", "180 degres", "270 degres", "360 degres"), 1),
    ("Si x + 5 = 12, combien vaut x ?", ("5", "6", "7", "8"), 2),
    ("Si 3x = 21, combien vaut x ?", ("6", "7", "8", "9"), 1),
    ("Quel est le PGCD de 8 et 12 ?", ("2", "4", "6", "8"), 1),
    ("Quel est le PPCM de 3 et 4 ?", ("7", "10", "12", "14"), 2),
    ("Quel nombre est premier ?", ("9", "15", "17", "21"), 2),
    (  ("Quel est le perimetre d'un carre de cote 5 cm ?", ("10 cm", "15 cm", "20 cm", "25 cm"), 2),
    ("Quelle est l'aire d'un rectangle de 6 cm sur 4 cm ?", ("10 cm2", "20 cm2", "24 cm2", "28 cm2"), 2),
])

QUESTION_BANKS_MATIERES["Histoire"] = _bank([
    ("En quelle annee la Revolution francaise commence-t-elle ?", ("1789", "1815", "1848", "1914"), 0),
    ("Quel evenement a lieu le 14 juillet 1789 ?", ("Bataille de Verdun", "Prise de la Bastille", "Armistice", "Congres de Vienne"), 1),
    ("Qui fut le premier empereur des Francais ?", ("Napoleon Bonaparte", "Louis XIV", "Charlemagne", "Henri IV"), 0),
    ("La Premiere Guerre mondiale commence en...", ("1905", "1912", "1914", "1918"), 2),
    ("La Seconde Guerre mondiale se termine en...", ("1939", "1942", "1945", "1950"), 2),
    ("Quelle civilisation a construit les pyramides de Gizeh ?", ("Romaine", "Egyptienne", "Grecque", "Maya"), 1),
    ("Qui etait Nelson Mandela ?", ("Un ecrivain francais", "Un dirigeant sud-africain", "Un empereur romain", "Un explorateur portugais"), 1),
    ("En quelle annee l'independance de la Guinee est-elle proclamee ?", ("1956", "1958", "1960", "1963"), 1),
    ("Qui fut le premier president de la Republique de Guinee ?", ("Ahmed Sekou Toure", "Modibo Keita", "Kwame Nkrumah", "Julius Nyerere"), 0),
    ("Quel empire ouest-africain avait Tombouctou comme grand centre intellectuel ?", ("Empire du Mali", "Empire romain", "Empire ottoman", "Empire aztèque"), 0),
    ("Qui est associe a la decouverte de l'Amerique en 1492 ?", ("Christophe Colomb", "Vasco de Gama", "Magellan", "James Cook"), 0),
    ("Quel peuple a developpe la democratie antique a Athenes ?", ("Grecs", "Vikings", "Mongols", "Romains"), 0),
    ("La Renaissance europeenne se developpe principalement a partir du...", ("XIVe siecle", "XVIIIe siecle", "XXe siecle", "XXIe siecle"), 0),
    ("Quel mur est devenu un symbole de la division de Berlin ?", ("Mur de Chine", "Mur de Berlin", "Mur d'Hadrien", "Mur d'Accra"), 1),
    ("La decolonisation de l'Afrique s'accelere surtout au...", ("XXe siecle", "XVe siecle", "XVIIe siecle", "XIIIe siecle"), 0),
    ("Quel evenement marque le debut de la Revolution industrielle ?", ("Developpement des machines et usines", "Invention de l'ecriture", "Chute de Rome", "Construction des pyramides"), 0),
    ("Qui etait Soundiata Keita ?", ("Un fondateur de l'Empire du Mali", "Un pharaon", "Un roi d'Angleterre", "Un explorateur chinois"), 0),
    ("Quel royaume africain est celebre pour ses bronzes historiques ?", ("Benin", "Suede", "Portugal", "Japon"), 0),
    ("Quel est le nom de la periode qui suit l'Antiquite ?", ("Moyen Age", "Renaissance", "Temps modernes", "Epoque contemporaine"), 0),
    ("La Guerre froide oppose principalement...", ("Etats-Unis et URSS", "France et Espagne", "Chine et Inde", "Egypte et Libye"), 0),
])

QUESTION_BANKS_MATIERES["Geographie"] = _bank([
    ("Quel est le plus grand continent ?", ("Afrique", "Asie", "Europe", "Oceanie"), 1),
    ("Quel est le plus grand ocean ?", ("Atlantique", "Indien", "Pacifique", "Arctique"), 2),
    ("Quelle est la capitale de la Guinee ?", ("Kankan", "Labe", "Conakry", "Kindia"), 2),
    ("Quel fleuve traverse l'Egypte ?", ("Nil", "Niger", "Congo", "Senegal"), 0),
    ("Quel desert est le plus vaste desert chaud du monde ?", ("Gobi", "Sahara", "Kalahari", "Atacama"), 1),
    ("Quel est le plus haut sommet du monde ?", ("Mont Blanc", "Everest", "Kilimandjaro", "K2"), 1),
    ("Quel pays a la plus grande superficie d'Afrique ?", ("Algerie", "Egypte", "Nigeria", "Ethiopie"), 0),
    ("Quel climat est caracteristique des regions proches de l'equateur ?", ("Equatorial", "Polaire", "Desertique", "Montagnard"), 0),
    ("Quelle ligne imaginaire partage la Terre en deux hemispheres ?", ("Tropique du Cancer", "Equateur", "Meridien de Greenwich", "Tropique du Capricorne"), 1),
    ("Le meridien de Greenwich sert de reference pour...", ("La longitude", "La latitude", "L'altitude", "La temperature"), 0),
    ("Quelle est la forme generale de la Terre ?", ("Plate", "Spherique", "Carree", "Triangulaire"), 1),
    ("Quel ocean borde la cote ouest de l'Afrique ?", ("Pacifique", "Atlantique", "Indien", "Arctique"), 1),
    ("Quelle est la capitale du Senegal ?", ("Dakar", "Bamako", "Niamey", "Bissau"), 0),
    ("Quelle est la capitale du Mali ?", ("Dakar", "Bamako", "Conakry", "Ouagadougou"), 1),
    ("Quel pays est appele le pays des mille collines ?", ("Rwanda", "Maroc", "Ghana", "Tunisie"), 0),
    ("Quel est le principal gaz de l'atmosphere terrestre ?", ("Oxygene", "Azote", "Hydrogene", "Helium"), 1),
    ("Comment appelle-t-on le mouvement de la Terre autour du Soleil ?", ("Rotation", "Revolution", "Translation lunaire", "Precession journaliere"), 1),
    ("La latitude mesure une distance par rapport a...", ("L'equateur", "Greenwich", "La Lune", "Un ocean"), 0),
    ("Quel continent est traverse par l'equateur ?", ("Afrique", "Europe", "Antarctique", "Australie uniquement"), 0),
    ("Une zone tres peuplee et fortement urbanisee est une...", ("Metropole", "Foret", "Dune", "Glacier"), 0),
])

QUESTION_BANKS_MATIERES["E.C.M"] = _bank([
    ("Que signifie citoyen ?", ("Personne ayant des droits et devoirs dans une communaute politique", "Personne sans droits", "Touriste uniquement", "Chef militaire"), 0),
    ("Quel est un droit fondamental ?", ("Droit a l'education", "Droit de voler", "Droit de tricher", "Droit de nuire"), 0),
    ("Quel est un devoir du citoyen ?", ("Respecter les lois", "Ignorer les lois", "Refuser toute responsabilite", "Detruire les biens publics"), 0),
    ("A quoi sert une Constitution ?", ("Organiser les institutions et definir des principes fondamentaux", "Fixer les prix du marche", "Remplacer toutes les lois scientifiques", "Choisir les equipes sportives"), 0),
    ("Que signifie democratie ?", ("Pouvoir exerce avec la participation des citoyens", "Pouvoir d'une seule famille", "Absence totale de regles", "Pouvoir militaire permanent"), 0),
    ("Quel est un symbole de la Republique de Guinee ?", ("Le drapeau national", "Une marque commerciale", "Un jeu video", "Une equipe etrangere"), 0),
    ("Pourquoi respecter le bien public ?", ("Parce qu'il appartient a la collectivite", "Parce qu'il appartient a une seule personne", "Parce qu'il est inutile", "Pour eviter l'ecole"), 0),
    ("Que signifie tolerance ?", ("Respecter les differences d'autrui", "Imposer son opinion", "Refuser toute discussion", "Insulter les autres"), 0),
    ("Quel comportement favorise la paix ?", ("Dialogue et respect", "Violence", "Menaces", "Discrimination"), 0),
    ("Qu'est-ce qu'une election ?", ("Un processus de choix de representants", "Une sanction scolaire", "Une reunion sportive", "Un recensement meteorologique"), 0),
    ("Que signifie egalite devant la loi ?", ("Les citoyens sont soumis aux memes regles juridiques", "Seuls les riches ont des droits", "Les lois ne concernent personne", "Chaque personne a une loi differente"), 0),
    ("Quel est le role d'un parlement dans un Etat ?", ("Participer au pouvoir legislatif", "Diriger les hopitaux uniquement", "Prevoir la meteo", "Organiser les matchs"), 0),
    ("Qu'est-ce qu'une responsabilite ?", ("Obligation d'assumer les consequences de ses actes", "Permission de tout faire", "Absence de devoir", "Refus de repondre"), 0),
    ("Que faut-il faire face a une information douteuse ?", ("La verifier avant de la partager", "La partager immediatement", "La modifier", "L'inventer"), 0),
    ("Quel comportement est civique ?", ("Respecter les autres et les biens communs", "Jeter des dechets partout", "Detruire les panneaux", "Refuser toute regle"), 0),
    ("Pourquoi payer certains impots ?", ("Contribuer au financement des services publics", "Acheter des votes", "Supprimer les ecoles", "Eviter toute loi"), 0),
    ("Que signifie discrimination ?", ("Traiter injustement une personne en raison d'une caracteristique", "Respecter tout le monde", "Aider une personne", "Dialoguer"), 0),
    ("Quelle institution rend generalement la justice ?", ("Les tribunaux", "Les clubs sportifs", "Les marches", "Les meteorologues"), 0),
    ("Quel principe aide a prevenir les conflits ?", ("Respect du droit et dialogue", "Vengeance", "Intimidation", "Censure de toute discussion"), 0),
    ("Quel est l'objectif principal de l'education civique ?", ("Former des citoyens responsables", "Apprendre uniquement le sport", "Remplacer les sciences", "Supprimer les devoirs"), 0),
])

QUESTION_BANKS_MATIERES["Sciences d'observation"] = _bank([
    ("Quel organe permet principalement de respirer ?", ("Poumons", "Estomac", "Rein", "Foie"), 0),
    ("Quel sens utilise les yeux ?", ("Ouie", "Vue", "Odorat", "Gout"), 1),
    ("Quel animal est un mammifere ?", ("Chien", "Poulet", "Poisson", "Grenouille"), 0),
    ("Quelle partie de la plante absorbe principalement l'eau du sol ?", ("Racines", "Fleurs", "Fruits", "Feuilles"), 0),
    ("Quel astre donne principalement sa lumiere a la Terre ?", ("La Lune", "Le Soleil", "Mars", "Venus"), 1),
    ("L'eau gele a environ...", ("0 degre C", "10 degres C", "50 degres C", "100 degres C"), 0),
    ("Quel etat de la matiere a une forme propre ?", ("Solide", "Liquide", "Gaz", "Vapeur uniquement"), 0),
    ("Quel organe pompe le sang ?", ("Coeur", "Poumon", "Cerveau", "Estomac"), 0),
    ("Quel gaz respirons-nous principalement avec l'air utile a notre organisme ?", ("Oxygene", "Helium", "Neon", "Hydrogene"), 0),
    ("Quelle source d'energie est renouvelable ?", ("Soleil", "Charbon", "Petrole", "Gaz naturel"), 0),
    ("Quel animal pond des oeufs ?", ("Poule", "Chat", "Chien", "Vache"), 0),
    ("Quel organe permet principalement de penser ?", ("Cerveau", "Coeur", "Poumon", "Rein"), 0),
    ("Quelle partie de la plante realise principalement la photosynthese ?", ("Feuille", "Racine", "Graine", "Ecorce"), 0),
    ("Quel astre est le satellite naturel de la Terre ?", ("Mars", "La Lune", "Le Soleil", "Jupiter"), 1),
    ("Quel changement transforme l'eau liquide en glace ?", ("Fusion", "Congelation", "Evaporation", "Condensation"), 1),
    ("Quel animal vit principalement dans l'eau ?", ("Poisson", "Cheval", "Lion", "Mouton"), 0),
    ("Quel organe filtre une grande partie des dechets du sang ?", ("Reins", "Poumons", "Yeux", "Oreilles"), 0),
    ("Pourquoi les plantes ont-elles besoin de lumiere ?", ("Pour realiser la photosynthese", "Pour entendre", "Pour marcher", "Pour respirer avec des poumons"), 0),
    ("Quel element est necessaire a la combustion ?", ("Oxygene", "Sable", "Bois uniquement", "Glace"), 0),
    ("Quelle est la planete la plus proche du Soleil ?", ("Mercure", "Terre", "Mars", "Jupiter"), 0),
])

QUESTION_BANKS_MATIERES["Biologie"] = _bank([
    ("Quelle est l'unite de base du vivant ?", ("Cellule", "Organe", "Tissu", "Organisme"), 0),
    ("Quel organite contient l'information genetique dans une cellule eucaryote ?", ("Noyau", "Vacuole", "Paroi", "Cytoplasme"), 0),
    ("Quel molecule transporte l'oxygene dans le sang ?", ("Hemoglobine", "Insuline", "Amidon", "ADN"), 0),
    ("Quel organe assure principalement les echanges gazeux ?", ("Poumons", "Foie", "Reins", "Estomac"), 0),
    ("Quel systeme assure le transport du sang ?", ("Systeme circulatoire", "Systeme digestif", "Systeme osseux", "Systeme excreteur"), 0),
    ("Quelle molecule porte l'information genetique ?", ("ADN", "Eau", "Glucose", "Oxygene"), 0),
    ("La mitose produit generalement...", ("Deux cellules filles", "Trois cellules", "Une cellule sans noyau", "Quatre cellules uniquement"), 0),
    ("Quel organe produit une grande partie de la bile ?", ("Foie", "Coeur", "Poumon", "Cerveau"), 0),
    ("Quel organe filtre le sang et produit l'urine ?", ("Rein", "Coeur", "Pancreas", "Poumon"), 0),
    ("Quel pigment permet aux plantes de capter la lumiere ?", ("Chlorophylle", "Hemoglobine", "Melanine", "Keratin"), 0),
    ("La photosynthese produit notamment...", ("Glucose et dioxygene", "Azote et sel", "Fer et calcium", "Alcool et methane"), 0),
    ("Quel systeme coordonne rapidement les reponses du corps ?", ("Systeme nerveux", "Systeme digestif", "Systeme urinaire", "Systeme osseux"), 0),
    ("Quel type de sang quitte le coeur vers les organes par les arteres systemiques ?", ("Sang oxygene", "Sang sans eau", "Sang uniquement digestif", "Sang sans cellules"), 0),
    ("Quel organe est principalement responsable de la digestion chimique dans l'estomac ?", ("Estomac", "Poumon", "Coeur", "Rein"), 0),
    ("Quel element constitue une grande partie des os ?", ("Calcium", "Mercure", "Helium", "Chlore gazeux"), 0),
    ("Comment appelle-t-on les cellules reproductrices ?", ("Gametes", "Neurones", "Globules rouges", "Plaquettes"), 0),
    ("Quel est le role principal des globules rouges ?", ("Transporter l'oxygene", "Produire la bile", "Digérer les aliments", "Former les os"), 0),
    ("Une relation entre deux especes dont une profite et l'autre est penalisee est...", ("Parasitisme", "Mutualisme", "Neutralisme", "Photosynthese"), 0),
    ("Quel organe endocrine produit l'insuline ?", ("Pancreas", "Foie", "Poumon", "Rate"), 0),
    ("Quel processus permet aux plantes vertes de fabriquer de la matiere organique avec la lumiere ?", ("Photosynthese", "Fermentation", "Respiration animale", "Digestion"), 0),
])

QUESTION_BANKS_MATIERES["Anglais"] = _bank([
    ("What is the French meaning of 'book'?", ("Livre", "Chaise", "Maison", "Table"), 0),
    ("Choose the correct form: 'She ___ to school every day.'", ("go", "goes", "going", "gone"), 1),
    ("What is the opposite of 'big'?", ("Tall", "Small", "Long", "Fast"), 1),
    ("What is the past of 'go'?", ("Goed", "Went", "Gone", "Going"), 1),
    ("Choose the correct article: '___ apple'", ("A", "An", "Thee", "At"), 1),
    ("What is the plural of 'child'?", ("Childs", "Children", "Childes", "Childrens"), 1),
    ("What does 'good morning' mean?", ("Bonsoir", "Bonjour", "Merci", "Au revoir"), 1),
    ("Choose the correct sentence.", ("He are happy.", "He is happy.", "He am happy.", "He be happy."), 1),
    ("What is the opposite of 'hot'?", ("Warm", "Cold", "Dry", "Bright"), 1),
    ("Which word is a verb?", ("Run", "Blue", "Table", "Slowly"), 0),
    ("Choose the correct form: 'They ___ football.'", ("plays", "play", "playing", "played"), 1),
    ("What is the past of 'eat'?", ("Eated", "Ate", "Eaten", "Eating"), 1),
    ("What does 'teacher' mean in French?", ("Medecin", "Professeur", "Ingenieur", "Agriculteur"), 1),
    ("Choose the correct pronoun: '___ am a student.'", ("He", "They", "I", "She"), 2),
    ("What is the comparative of 'small'?", ("Smallest", "Smaller", "More small", "Smalling"), 1),
    ("Choose the correct form: 'We ___ friends.'", ("is", "am", "are", "be"), 2),
    ("What is the meaning of 'water'?", ("Feu", "Eau", "Air", "Terre"), 1),
    ("Choose the correct question word for a place.", ("When", "Where", "Why", "Who"), 1),
    ("What is the past of 'see'?", ("Saw", "Seed", "Seen", "Seeed"), 0),
    ("Choose the correct sentence.", ("I have two brothers.", "I has two brothers.", "I having two brothers.", "I am have two brothers."), 0),
])

QUESTION_BANKS_MATIERES["Physique et Chimie"] = _bank([
    ("Quelle est l'unite SI de la longueur ?", ("Metre", "Litre", "Seconde", "Newton"), 0),
    ("Quelle est l'unite SI de la masse ?", ("Kilogramme", "Metre", "Ampere", "Pascal"), 0),
    ("Quelle est l'unite de la force ?", ("Joule", "Newton", "Watt", "Volt"), 1),
    ("Quelle est la formule de la vitesse moyenne ?", ("v=d/t", "v=t/d", "v=d+t", "v=d-t"), 0),
    ("Quelle particule porte une charge negative ?", ("Proton", "Neutron", "Electron", "Noyau"), 2),
    ("Quel est le symbole chimique de l'oxygene ?", ("O", "Ox", "Og", "C"), 0),
    ("Quel est le symbole du sodium ?", ("S", "So", "Na", "Sd"), 2),
    ("L'eau pure a environ quel pH ?", ("2", "5", "7", "12"), 2),
    ("Quelle forme d'energie possede un objet en mouvement ?", ("Cinétique", "Chimique uniquement", "Nucleaire uniquement", "Statique uniquement"), 0),
    ("Quel appareil mesure la tension electrique ?", ("Amperemetre", "Voltmeter", "Balance", "Thermometre"), 1),
    ("Quel appareil mesure l'intensite du courant ?", ("Amperemetre", "Voltmeter", "Regle", "Barometre"), 0),
    ("Quel est le symbole du fer ?", ("Fe", "F", "Fr", "Ir"), 0),
    ("Une solution homogene contient...", ("Un solvant et un ou plusieurs solutes repartis uniformement", "Deux solides seulement", "Un gaz pur uniquement", "Aucun liquide"), 0),
    ("Quel changement passe de liquide a gaz ?", ("Fusion", "Evaporation", "Solidification", "Condensation"), 1),
    ("Quel changement passe de gaz a liquide ?", ("Condensation", "Fusion", "Sublimation", "Evaporation"), 0),
    ("Quel est le role d'un fusible ?", ("Proteger un circuit contre une surintensite", "Augmenter la masse", "Mesurer la temperature", "Produire de l'eau"), 0),
    ("Dans un circuit en serie, le courant est...", ("Le meme dans les composants successifs", "Toujours nul", "Different dans chaque point", "Independamment choisi"), 0),
    ("Quelle grandeur se mesure en volts ?", ("Tension", "Masse", "Force", "Energie"), 0),
    ("Quelle grandeur se mesure en joules ?", ("Energie", "Intensite", "Longueur", "Masse"), 0),
    ("Quelle particule est electriquement neutre ?", ("Electron", "Proton", "Neutron", "Ion positif"), 2),
])

QUESTION_BANKS_MATIERES["Physique"] = _bank([
    ("Quelle est l'unite SI de la force ?", ("Newton", "Joule", "Watt", "Volt"), 0),
    ("Quelle est l'expression de la vitesse ?", ("v=d/t", "v=t/d", "v=d*t", "v=d+t"), 0),
    ("Quelle grandeur se mesure en kilogrammes ?", ("Masse", "Force", "Energie", "Puissance"), 0),
    ("Quelle grandeur se mesure en secondes ?", ("Temps", "Masse", "Longueur", "Tension"), 0),
    ("Quelle est l'unite SI de l'energie ?", ("Joule", "Newton", "Watt", "Pascal"), 0),
    ("Quelle est l'unite SI de la puissance ?", ("Watt", "Volt", "Ampere", "Ohm"), 0),
    ("Quelle est l'unite SI de la tension ?", ("Volt", "Watt", "Newton", "Joule"), 0),
    ("Quelle est l'unite SI de l'intensite ?", ("Ampere", "Volt", "Ohm", "Tesla"), 0),
    ("Quelle force attire les objets vers la Terre ?", ("Gravitation", "Frottement nul", "Poussee magnetique", "Pression"), 0),
    ("Quel instrument mesure une temperature ?", ("Thermometre", "Voltmeter", "Amperemetre", "Dynamometre"), 0),
    ("Quel instrument mesure une force ?", ("Dynamometre", "Balance", "Regle", "Barometre"), 0),
    ("Dans le vide, la lumiere se propage environ a...", ("3 x 10^8 m/s", "3 x 10^5 m/s", "300 m/s", "30 m/s"), 0),
    ("Quel type de mouvement a une vitesse constante sur une trajectoire droite ?", ("Mouvement rectiligne uniforme", "Mouvement circulaire uniforme", "Mouvement aleatoire", "Repos"), 0),
    ("Quelle energie est liee a la hauteur d'un objet ?", ("Energie potentielle gravitationnelle", "Energie sonore", "Energie nucleaire uniquement", "Energie chimique uniquement"), 0),
    ("Quelle energie est liee au mouvement ?", ("Energie cinetique", "Energie potentielle", "Energie chimique uniquement", "Energie lumineuse uniquement"), 0),
    ("Un objet immobile a une vitesse...", ("Nulle", "Infinie", "Negative obligatoirement", "Toujours egale a 1"), 0),
    ("La frequence se mesure en...", ("Hertz", "Newton", "Joule", "Metre"), 0),
    ("Le son a besoin d'un milieu materiel pour se propager ?", ("Oui", "Non", "Seulement dans le vide", "Seulement dans l'espace"), 0),
    ("Quelle loi relie tension, resistance et intensite ?", ("Loi d'Ohm", "Loi de Boyle", "Loi de Snell uniquement", "Loi de Dalton"), 0),
    ("Si une force nette agit sur un objet, elle peut modifier...", ("Son mouvement", "Sa couleur uniquement", "Son nom", "Son age"), 0),
])

QUESTION_BANKS_MATIERES["Chimie"] = _bank([
    ("Quel est le symbole de l'hydrogene ?", ("H", "Hy", "Hg", "Ho"), 0),
    ("Quel est le symbole de l'oxygene ?", ("O", "Ox", "Og", "O2 uniquement"), 0),
    ("Quel est le symbole du carbone ?", ("C", "Ca", "Co", "Cr"), 0),
     ("Quel est le symbole du fer ?", ("Fe", "F", "Fr", "Ir"), 0),
    ("Quel est le symbole du sodium ?", ("Na", "So", "S", "Sd"), 0),
    ("Quel est le symbole du chlore ?", ("Cl", "Ch", "C", "Cr"), 0),
    ("Une substance de pH inferieur a 7 est generalement...", ("Acide", "Basique", "Neutre", "Metallique"), 0),
    ("Une substance de pH superieur a 7 est generalement...", ("Acide", "Basique", "Neutre", "Solide"), 1),
    ("Une solution de pH 7 est...", ("Neutre", "Acide forte", "Basique forte", "Toujours gazeuse"), 0),
    ("Quel est le solvant principal de l'eau sucree ?", ("Eau", "Sucre", "Sel", "Oxygene"), 0),
    ("Quel gaz est necessaire a une combustion ordinaire ?", ("Oxygene", "Azote", "Helium", "Argon"), 0),
    ("Quel est le nom de H2O ?", ("Eau", "Oxygene", "Hydrogene", "Peroxyde"), 0),
    ("Combien d'atomes d'hydrogene contient H2O ?", ("1", "2", "3", "4"), 1),
    ("Combien d'atomes d'oxygene contient CO2 ?", ("1", "2", "3", "4"), 1),
    ("La matiere est composee notamment de...", ("Atomes et molecules", "Uniquement de lumiere", "Uniquement de vide", "Uniquement de sons"), 0),
    ("Quel changement forme un solide a partir d'un liquide ?", ("Solidification", "Fusion", "Evaporation", "Sublimation"), 0),
    ("Quel changement forme un liquide a partir d'un solide ?", ("Fusion", "Solidification", "Condensation", "Sublimation inverse"), 0),
    ("Une molecule est un ensemble d'...", ("Atomes lies", "Planetes", "Organes", "Cellules uniquement"), 0),
    ("Quel instrument sert a mesurer une masse au laboratoire ?", ("Balance", "Thermometre", "pH-metre uniquement", "Boussole"), 0),
    ("Quel gaz est le plus abondant dans l'atmosphere terrestre ?", ("Azote", "Oxygene", "Hydrogene", "Dioxyde de carbone"), 0),
])

QUESTION_BANKS_MATIERES["Economie"] = _bank([
    ("Qu'est-ce qu'un besoin economique ?", ("Un besoin dont la satisfaction mobilise des ressources limitees", "Un objet sans utilite", "Une loi physique", "Un sport"), 0),
    ("Que signifie PIB ?", ("Produit interieur brut", "Prix international brut", "Production industrielle bancaire", "Produit import-export brut"), 0),
    ("Qu'est-ce que l'inflation ?", ("Hausse generale et durable du niveau des prix", "Baisse des salaires uniquement", "Hausse d'une seule entreprise", "Disparition de la monnaie"), 0),
    ("Qu'est-ce qu'un marche ?", ("Un lieu ou systeme de rencontre entre offre et demande", "Une banque uniquement", "Une usine uniquement", "Une ecole"), 0),
    ("L'offre represente principalement...", ("Les quantites que les vendeurs souhaitent proposer", "Les besoins des acheteurs uniquement", "Les impots", "Les salaires publics"), 0),
    ("La demande represente principalement...", ("Les quantites que les acheteurs souhaitent acquérir", "Les stocks des producteurs uniquement", "Les exportations seulement", "Les routes"), 0),
    ("Qu'est-ce qu'un bien ?", ("Un produit ou objet pouvant satisfaire un besoin", "Une dette uniquement", "Une taxe", "Une monnaie etrangere"), 0),
    ("Quel agent economique consomme principalement des biens et services ?", ("Menages", "Banques centrales uniquement", "Entreprises publiques uniquement", "Douanes uniquement"), 0),
    ("Quel agent produit principalement des biens et services marchands ?", ("Entreprises", "Menages uniquement", "Ecoles uniquement", "Touristes"), 0),
    ("Que signifie chomage ?", ("Situation d'une personne sans emploi qui recherche un emploi selon une definition statistique", "Toute personne en vacances", "Tout eleve", "Toute personne agee"), 0),
    ("Qu'est-ce qu'un investissement ?", ("Une depense destinee notamment a accroitre les capacites de production", "Une consommation alimentaire", "Un impôt", "Un salaire"), 0),
    ("Quel est le role principal d'une banque commerciale ?", ("Collecter des depots et accorder des credits", "Produire du petrole", "Construire des routes uniquement", "Fixer toutes les lois"), 0),
    ("Que sont les exportations ?", ("Biens et services vendus a l'etranger", "Biens achetes a l'etranger", "Impots nationaux", "Salaires"), 0),
    ("Que sont les importations ?", ("Biens et services achetes a l'etranger", "Biens vendus a l'etranger", "Taxes locales", "Epargne uniquement"), 0),
    ("Qu'est-ce que la monnaie ?", ("Un instrument servant notamment d'echange, d'unite de compte et de reserve de valeur", "Un produit agricole", "Une machine", "Une ressource minière uniquement"), 0),
    ("Quand la demande augmente et que l'offre reste identique, le prix peut...", ("Augmenter", "Toujours diminuer", "Devenir nul", "Disparaitre"), 0),
    ("Qu'est-ce que l'epargne ?", ("Part du revenu non consommee immediatement", "Une dette obligatoire", "Une taxe", "Une importation"), 0),
    ("Qu'est-ce qu'une taxe ?", ("Prelevement obligatoire effectue par une autorite publique", "Un cadeau", "Un salaire", "Une exportation"), 0),
    ("La productivite mesure notamment...", ("La quantite produite par unite de facteur utilise", "Le nombre de vacances", "Le niveau de pluie", "La population uniquement"), 0),
    ("Que signifie rarete en economie ?", ("Les ressources disponibles sont limitees par rapport aux besoins", "Les ressources sont infinies", "Les besoins n'existent pas", "Les prix sont toujours nuls"), 0),
])

QUESTION_BANKS_MATIERES["Philosophie"] = _bank([
    ("Qu'est-ce que la philosophie cherche principalement a developper ?", ("Une reflexion rationnelle et critique", "La memorisation sans reflexion", "La vitesse sportive", "La prediction meteorologique"), 0),
    ("Que signifie raisonner ?", ("Enchainer des idees de maniere logique", "Reciter sans comprendre", "Dormir", "Imiter"), 0),
    ("Quel concept concerne la capacite de choisir entre plusieurs possibilites ?", ("Liberte", "Matiere", "Vitesse", "Volume"), 0),
    ("La verite concerne principalement...", ("La conformite d'un jugement au reel selon un critere donne", "La popularite d'une personne", "La force physique", "La richesse"), 0),
    ("Qu'est-ce qu'une opinion ?", ("Un jugement ou une croyance qui n'est pas necessairement demontre", "Une preuve mathematique", "Une loi physique", "Une unite de mesure"), 0),
    ("Qu'est-ce qu'un argument ?", ("Une raison avancee pour soutenir une idee", "Une emotion uniquement", "Une question sans objet", "Un chiffre aleatoire"), 0),
    ("Le doute philosophique peut servir a...", ("Examiner les certitudes et rechercher de meilleures raisons", "Eviter toute pensee", "Refuser toute preuve", "Supprimer le dialogue"), 0),
    ("Que signifie conscience ?", ("Capacite de se representer soi-meme et son experience", "Force musculaire", "Vitesse de marche", "Capacite de calcul uniquement"), 0),
    ("L'ethique s'interesse principalement...", ("A la reflexion sur le bien, le mal et l'action", "A la mesure des distances", "A la chimie", "A la meteorologie"), 0),
    ("La politique concerne notamment...", ("L'organisation de la vie collective et du pouvoir", "La digestion", "La rotation terrestre", "La classification des roches"), 0),
    ("Qu'est-ce qu'une demonstration ?", ("Un raisonnement qui etablit une conclusion a partir d'elements justifies", "Une opinion populaire", "Une emotion", "Une hypothese sans raison"), 0),
    ("Quel concept oppose souvent apparence et realite ?", ("Verite", "Vitesse", "Temperature", "Masse"), 0),
    ("Pourquoi definir un concept ?", ("Pour preciser son sens et eviter les confusions", "Pour le rendre plus long", "Pour supprimer la discussion", "Pour changer son sens au hasard"), 0),
    ("Qu'est-ce qu'un prejugé ?", ("Un jugement forme avant un examen suffisant", "Une preuve scientifique", "Une conclusion necessaire", "Une mesure"), 0),
    ("La logique etudie principalement...", ("La validite des raisonnements", "Les roches", "Les oceans", "Les muscles"), 0),
    ("Une question philosophique est souvent...", ("Generale et ouverte a l'argumentation", "Uniquement numerique", "Toujours repondue par oui", "Sans rapport avec les concepts"), 0),
    ("Que signifie autonomie ?", ("Capacite de se donner ou suivre rationnellement ses propres regles", "Obeissance aveugle", "Absence de pensee", "Force physique"), 0),
    ("Quel est le role du dialogue philosophique ?", ("Confronter les arguments et clarifier les idees", "Eviter les arguments", "Imposer une opinion", "Remplacer les preuves"), 0),
    ("Qu'est-ce qu'une hypothese ?", ("Une proposition provisoire a examiner", "Une conclusion definitive", "Une loi obligatoire", "Une definition toujours vraie"), 0),
    ("Penser de maniere critique signifie notamment...", ("Examiner les raisons, les preuves et les objections", "Tout refuser sans examen", "Croire toute information", "Eviter les questions"), 0),
])

QUESTION_BANKS_MATIERES["Geologie"] = _bank([
    ("Qu'etudie principalement la geologie ?", ("La Terre, ses roches et son histoire", "Les langues", "Les monnaies", "Les elections"), 0),
    ("Quelle couche est au centre de la Terre ?", ("Noyau", "Croute", "Atmosphere", "Hydrosphere"), 0),
    ("Quelle couche superficielle solide appartient a la lithosphere ?", ("Croute terrestre", "Noyau externe", "Noyau interne", "Atmosphere"), 0),
    ("Comment appelle-t-on une roche formee par refroidissement d'un magma ?", ("Roche magmatique", "Roche sedimentaire", "Roche biologique uniquement", "Roche artificielle"), 0),
    ("Comment se forme une roche sedimentaire ?", ("Par accumulation et consolidation de sediments notamment", "Uniquement par fusion", "Uniquement par evaporation de metaux", "Par combustion"), 0),
    ("Quel processus transforme une roche sous pression et temperature sans fusion complete ?", ("Metamorphisme", "Evaporation", "Photosynthese", "Condensation"), 0),
    ("Quel instrument permet d'enregistrer les vibrations sismiques ?", ("Sismographe", "Thermometre", "Barometre", "Voltmeter"), 0),
    ("Quel phenomene peut provoquer un tsunami ?", ("Un seisme sous-marin important", "Une simple pluie", "Une eclipse", "Une brise"), 0),
    ("Les plaques tectoniques se deplacent sur...", ("L'asthenosphere", "La troposphere", "Le noyau interne", "Les oceans uniquement"), 0),
    ("Qu'est-ce qu'un volcan ?", ("Une ouverture de la croute permettant la remontee de materiaux magmatiques", "Un glacier", "Une riviere", "Une faille artificielle"), 0),
    ("Quel mineral est tres courant dans le quartz ?", ("Silice", "Fer pur uniquement", "Or uniquement", "Sodium pur uniquement"), 0),
    ("Quel processus erode les roches ?", ("Erosion", "Photosynthese", "Respiration", "Fermentation"), 0),
    ("Quel agent peut transporter des sediments ?", ("Eau", "Uniquement la lumiere", "Le vide", "Un champ magnetique seul"), 0),
    ("Quelle echelle est historiquement utilisee pour classer la durete des mineraux ?", ("Mohs", "Richter", "Beaufort", "Celsius"), 0),
    ("Le granite est une roche...", ("Magmatique", "Sedimentaire", "Metamorphique uniquement", "Organique"), 0),
    ("Le calcaire est generalement une roche...", ("Sedimentaire", "Magmatique profonde", "Volcanique uniquement", "Metallique"), 0),
    ("Quel gaz est libere en grande quantite par certains volcans ?", ("Vapeur d'eau", "Helium pur uniquement", "Oxygene pur uniquement", "Neon pur uniquement"), 0),
    ("Une faille est principalement...", ("Une fracture de la croute accompagnee d'un deplacement", "Une montagne", "Une riviere", "Un nuage"), 0),
    ("Les fossiles servent notamment a etudier...", ("Les formes de vie anciennes et l'histoire de la Terre", "Les taux de change", "Les lois electorales", "La vitesse du son"), 0),
    ("Quel mouvement des plaques peut former une chaine de montagnes ?", ("Convergence", "Eloignement sans interaction", "Rotation de la Lune", "Evaporation"), 0),
])

# Associe automatiquement chaque niveau/matiere a sa banque specialisee si aucune
# banque plus precise n'existe deja. Les banques existantes (par exemple Maths
# de 1ere A, 10eme A et Terminale A SM) restent prioritaires.
for _niveau in NIVEAUX_PRIMAIRE + NIVEAUX_COLLEGE + NIVEAUX_LYCEE:
    _matieres = PRIMAIRE_MATIERES if _niveau in NIVEAUX_PRIMAIRE else (COLLEGE_MATIERES if _niveau in NIVEAUX_COLLEGE else [])
    for _matiere in _matieres:
        if (_niveau, _matiere) not in QUESTION_BANKS and _matiere in QUESTION_BANKS_MATIERES:
            QUESTION_BANKS[(_niveau, _matiere)] = list(QUESTION_BANKS_MATIERES[_matiere])

for _serie in SERIES_LYCEE:
    _matieres = LYCEE_SS_MATIERES if _serie == "SS" else LYCEE_SM_SE_MATIERES
    for _niveau_base in NIVEAUX_LYCEE:
        _niveau = "{} ({})".format(_niveau_base, _serie)
        for _matiere in _matieres:
            if (_niveau, _matiere) not in QUESTION_BANKS and _matiere in QUESTION_BANKS_MATIERES:
                QUESTION_BANKS[(_niveau, _matiere)] = list(QUESTION_BANKS_MATIERES[_matiere])

# Controle de securite : chaque banque utilisee par le menu doit contenir
# au moins 20 questions. Une erreur est levee au lancement plutot que d'afficher
# un quiz incomplet.
for _key, _bank_data in QUESTION_BANKS.items():
    if len(_bank_data) < QUESTIONS_PAR_QUIZ:
        raise ValueError("Banque insuffisante pour {} : {}".format(_key, len(_bank_data)))

# ============================================================
#  WIDGETS REUTILISABLES
# ============================================================

class GradientBackground(Widget):
    """Fond en degrade vertical."""

    def __init__(self, color_top=BG_DARK_2, color_bottom=BG_DARK_1, **kwargs):
        super().__init__(**kwargs)
       self.color_top = color_top
        self.color_bottom = color_bottom
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self._build_gradient_texture()
        self.bind(pos=self._update, size=self._update)

    def _build_gradient_texture(self):
        from kivy.graphics.texture import Texture
        steps = 64
        buf = bytearray()
        for i in range(steps):
            t = i / (steps - 1)
            r = self.color_top[0] + (self.color_bottom[0] - self.color_top[0]) * t
            g = self.color_top[1] + (self.color_bottom[1] - self.color_top[1]) * t
            b = self.color_top[2] + (self.color_bottom[2] - self.color_top[2]) * t
            buf += bytes([int(r * 255), int(g * 255), int(b * 255), 255])
        tex = Texture.create(size=(1, steps), colorfmt="rgba")
        tex.blit_buffer(bytes(buf), colorfmt="rgba", bufferfmt="ubyte")
        tex.wrap = "clamp_to_edge"
        self.rect.texture = tex

    def _update(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class Card3DButton(FloatLayout):
    """Bouton d'action avec ombre portee (utilise pour ENTRER, SUIVANT, RETOUR...)."""

    def __init__(self, text="", on_release=None, bg_color=CARD_BG,
                 text_color=TEXT_LIGHT, font_size=dp(18), bold=True, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = self.size_hint if "size_hint" in kwargs else (None, None)
        self._on_release_cb = on_release

        with self.canvas.before:
            Color(*CARD_SHADOW, 0.55)
            self.shadow = RoundedRectangle(radius=[dp(14)])
            self._bg_color_inst = Color(*bg_color)
            self.bg = RoundedRectangle(radius=[dp(14)])

        self.label = Label(text=text, color=text_color, font_size=font_size,
                            bold=bold, halign="center", valign="middle")
        self.add_widget(self.label)
        self.bind(pos=self._update_graphics, size=self._update_graphics)

    def _update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.shadow.pos = (self.x + dp(2), self.y - dp(5))
        self.shadow.size = self.size
        self.label.pos = self.pos
        self.label.size = self.size
        self.label.text_size = self.size

    def set_text(self, text):
        self.label.text = text

    def set_bg_color(self, color):
        self._bg_color_inst.rgba = list(color)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            Animation(pos=(self.x + dp(1), self.y - dp(3)), duration=0.06).start(self)
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            Animation(pos=(self.x - dp(1), self.y + dp(3)), duration=0.08).start(self)
            if self._on_release_cb:
                self._on_release_cb()
            return True
        return super().on_touch_up(touch)


class ListRow(FloatLayout):
    """Ligne pleine largeur : barre d'accent + texte + valeur/fleche a droite.
    Utilisee pour le menu, les infos et les parametres."""

    def __init__(self, text="", right_text=">", accent_color=ACCENT,
                 interactive=True, on_release=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = self.size_hint if "size_hint" in kwargs else (1, None)
        self.interactive = interactive
        self._on_release_cb = on_release
        self._base_bg = list(CARD_BG)
        self._pressed_bg = list(ACCENT_DARK)

        with self.canvas.before:
            self._bg_color_inst = Color(*self._base_bg)
            self.bg = RoundedRectangle(radius=[dp(10)])
            Color(*accent_color)
            self.accent = RoundedRectangle(radius=[dp(3)])
            Color(*BG_DARK_1)
            self.divider = Rectangle()

        self.label = Label(text=text, color=TEXT_LIGHT, font_size=dp(16),
                            bold=True, halign="left", valign="middle")
        self.right_label = Label(text=right_text, color=TEXT_MUTED, font_size=dp(15),
                                  bold=True, halign="right", valign="middle")
        self.add_widget(self.label)
        self.add_widget(self.right_label)
        self.bind(pos=self._update_graphics, size=self._update_graphics)

    def _update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.accent.pos = (self.x + dp(6), self.y + dp(8))
        self.accent.size = (dp(4), self.height - dp(16))
        self.divider.pos = (self.x, self.y - dp(1))
        self.divider.size = (self.width, dp(1))

        self.label.pos = (self.x + dp(22), self.y)
        self.label.size = (self.width * 0.55, self.height)
        self.label.text_size = self.label.size

        self.right_label.pos = (self.x + self.width * 0.55, self.y)
        self.right_label.size = (self.width * 0.42, self.height)
        self.right_label.text_size = self.right_label.size

    def set_right_text(self, value):
        self.right_label.text = value

    def on_touch_down(self, touch):
        if self.interactive and self.collide_point(*touch.pos):
            self._bg_color_inst.rgba = self._pressed_bg
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.interactive and self.collide_point(*touch.pos):
            self._bg_color_inst.rgba = self._base_bg
            if self._on_release_cb:
                self._on_release_cb()
            return True
        return super().on_touch_up(touch)


class CandidateResultRow(FloatLayout):
    """Ligne de classement claire et entièrement cliquable."""
    def __init__(self, candidate=None, on_release=None, **kwargs):
        super().__init__(**kwargs)
        self.candidate = candidate or {}
        self._on_release_cb = on_release
        self.size_hint = self.size_hint if "size_hint" in kwargs else (1, None)
        self.height = kwargs.get("height", dp(72))
        self._normal = list(CARD_BG)
        self._pressed = list(ACCENT_DARK)
        me = not self.candidate.get("ia", True)
        with self.canvas.before:
            self._bg_color_inst = Color(*(list(ACCENT_DARK) if me else self._normal))
            self.bg = RoundedRectangle(radius=[dp(10)])
            Color(*(GOLD if me else ACCENT))
            self.accent = RoundedRectangle(radius=[dp(3)])

        rank = self.candidate.get("rank", "-")
        name = self.candidate.get("name", "Candidat")
        score = int(self.candidate.get("score", 0))
        total = int(self.candidate.get("total", 0))
        moyenne = (score / total * 20.0) if total else 0.0
        statut = "ADMIS" if moyenne >= 10.0 else "ÉCHOUÉ"

        self.name_label = Label(
            text="#{}  {}".format(rank, name), color=TEXT_LIGHT, font_size=dp(16),
            bold=True, halign="left", valign="middle")
        self.info_label = Label(
            text="Moyenne : {:.2f}/20   •   Score : {}/{}   •   {}".format(
                moyenne, score, total, statut),
            color=GREEN if statut == "ADMIS" else RED, font_size=dp(13),
            bold=True, halign="left", valign="middle")
        self.hint_label = Label(text="VOIR LA CORRECTION  >", color=GOLD,
                                font_size=dp(11), bold=True, halign="right", valign="middle")
        self.add_widget(self.name_label)
        self.add_widget(self.info_label)
        self.add_widget(self.hint_label)
        self.bind(pos=self._update_graphics, size=self._update_graphics)

    def _update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.accent.pos = (self.x + dp(6), self.y + dp(9))
        self.accent.size = (dp(4), self.height - dp(18))
        self.name_label.pos = (self.x + dp(22), self.y + dp(31))
        self.name_label.size = (self.width - dp(45), dp(30))
        self.name_label.text_size = self.name_label.size
        self.info_label.pos = (self.x + dp(22), self.y + dp(6))
        self.info_label.size = (self.width - dp(170), dp(24))
        self.info_label.text_size = self.info_label.size
        self.hint_label.pos = (self.x + self.width - dp(160), self.y + dp(6))
        self.hint_label.size = (dp(150), dp(24))
        self.hint_label.text_size = self.hint_label.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._bg_color_inst.rgba = self._pressed
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self._bg_color_inst.rgba = list(ACCENT_DARK if not self.candidate.get("ia", True) else CARD_BG)
            if self._on_release_cb:
                self._on_release_cb(self.candidate)
            return True
        return super().on_touch_up(touch)


class FlashcardRow(FloatLayout):
    """Fiche de revision : touche pour reveler/masquer la reponse."""

    def __init__(self, question="", answer="", **kwargs):
        super().__init__(**kwargs)
        self.size_hint = self.size_hint if "size_hint" in kwargs else (1, None)
        self.question = question
        self.answer = answer
        self.revealed = False

        with self.canvas.before:
            self._bg_color_inst = Color(*CARD_BG)
            self.bg = RoundedRectangle(radius=[dp(12)])
            Color(*GOLD)
            self.accent = RoundedRectangle(radius=[dp(3)])

        self.label = Label(text=question, color=TEXT_LIGHT, font_size=dp(15),
                            bold=True, halign="left", valign="middle")
        self.hint = Label(text="Toucher pour voir", color=TEXT_MUTED, font_size=dp(12),
                           halign="right", valign="middle")
        self.add_widget(self.label)
        self.add_widget(self.hint)
        self.bind(pos=self._update_graphics, size=self._update_graphics)

    def _update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.accent.pos = (self.x + dp(6), self.y + dp(10))
        self.accent.size = (dp(4), self.height - dp(20))

        self.label.pos = (self.x + dp(22), self.y)
        self.label.size = (self.width * 0.68, self.height)
        self.label.text_size = self.label.size

        self.hint.pos = (self.x + self.width * 0.68, self.y)
        self.hint.size = (self.width * 0.28, self.height)
        self.hint.text_size = self.hint.size

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.revealed = not self.revealed
            if self.revealed:
                self.label.text = "-> " + self.answer
                self.label.color = GOLD
                self.hint.text = "Toucher pour cacher"
                self._bg_color_inst.rgba = list(ACCENT_DARK)
            else:
                self.label.text = self.question
                self.label.color = TEXT_LIGHT
                self.hint.text = "Toucher pour voir"
                self._bg_color_inst.rgba = list(CARD_BG)
            return True
        return super().on_touch_up(touch)


class AnswerOptionRow(FloatLayout):
    """Option de reponse pour le quiz/examen (texte centre, se colore apres reponse)."""

    def __init__(self, text="", index=0, on_select=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = self.size_hint if "size_hint" in kwargs else (1, None)
        self.index = index
        self.locked = False
        self._on_select_cb = on_select

        with self.canvas.before:
            self._bg_color_inst = Color(*CARD_BG)
            self.bg = RoundedRectangle(radius=[dp(10)])

        self.label = Label(text=text, color=TEXT_LIGHT, font_size=dp(15),
                            bold=True, halign="left", valign="middle")
        self.add_widget(self.label)
        self.bind(pos=self._update_graphics, size=self._update_graphics)

    def _update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.label.pos = (self.x + dp(18), self.y)
        self.label.size = (self.width - dp(36), self.height)
        self.label.text_size = self.label.size

    def set_state(self, state):
        self.locked = True
        if state == "correct":
            self._bg_color_inst.rgba = list(GREEN)
        elif state == "wrong":
            self._bg_color_inst.rgba = list(RED)

    def reset_state(self):
        self.locked = False
        self._bg_color_inst.rgba = list(CARD_BG)

    def on_touch_up(self, touch):
        if not self.locked and self.collide_point(*touch.pos):
            if self._on_select_cb:
                self._on_select_cb(self.index, self)
            return True
        return super().on_touch_up(touch)


def make_header(title, on_back):
    """Barre d'en-tete commune : bouton RETOUR + titre."""
    header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(46), spacing=dp(10))
    back_btn = Card3DButton(text="<", bg_color=BG_DARK_1, text_color=TEXT_MUTED,
                             font_size=dp(16), size_hint=(None, 1), width=dp(46),
                             on_release=on_back)
    title_label = Label(text=title, color=TEXT_LIGHT, font_size=dp(20), bold=True,
                         halign="left", valign="middle")
    title_label.bind(size=lambda w, s: setattr(w, "text_size", s))
    header.add_widget(back_btn)
    header.add_widget(title_label)
    header.title_label = title_label
    return header


class TabBar(BoxLayout):
    """Barre d'onglets horizontale (ex: PRIMAIRE / COLLEGE / LYCEE ou SM / SS / SE)."""

    def __init__(self, tabs, on_select, active_index=0, **kwargs):
        super().__init__(orientation="horizontal", spacing=dp(8), size_hint=(1, None),
                          height=dp(46), **kwargs)
        self.tabs = tabs
        self.on_select_cb = on_select
        self.active_index = active_index
        self.buttons = []
        for i, label in enumerate(tabs):
            btn = Card3DButton(
                text=label, bg_color=(ACCENT if i == active_index else CARD_BG),
                text_color=TEXT_LIGHT, font_size=dp(13), bold=True,
                size_hint=(1, 1), on_release=lambda idx=i: self.select(idx))
            self.buttons.append(btn)
            self.add_widget(btn)

    def select(self, index):
        self.active_index = index
        for i, btn in enumerate(self.buttons):
            btn.set_bg_color(ACCENT if i == index else CARD_BG)
        if self.on_select_cb:
            self.on_select_cb(index, self.tabs[index])


# ============================================================
#  ECRAN D'ACCUEIL
# ============================================================

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        root.add_widget(GradientBackground())

        content = BoxLayout(orientation="vertical", spacing=dp(18), size_hint=(0.86, None),
                             pos_hint={"center_x": 0.5, "center_y": 0.5})
        content.bind(minimum_height=content.setter("height"))

        title = Label(text="QUIZ KOLIE", font_size=dp(40), bold=True, color=TEXT_LIGHT,
                      size_hint=(1, None), height=dp(60))
        subtitle = Label(text="Bienvenue !", font_size=dp(20), bold=True, color=GOLD,
                          size_hint=(1, None), height=dp(34))
        message = Label(text=("Teste tes connaissances, revise tes cours\n"
                               "et prepare tes examens en toute simplicite."),
                         font_size=dp(15), color=TEXT_MUTED, halign="center", valign="middle",
                         size_hint=(1, None), height=dp(70))
        message.bind(size=lambda w, s: setattr(w, "text_size", s))

        spacer_top = Widget(size_hint=(1, None), height=dp(10))
        enter_btn = Card3DButton(text="ENTRER", bg_color=ACCENT, text_color=TEXT_LIGHT,
                                  font_size=dp(20), size_hint=(1, None), height=dp(58),
                                  on_release=self.go_to_menu)

        content.add_widget(title)
        content.add_widget(subtitle)
        content.add_widget(message)
        content.add_widget(spacer_top)
        content.add_widget(enter_btn)
        root.add_widget(content)

        footer = Label(text="v1.0", font_size=dp(12), color=TEXT_MUTED, size_hint=(1, None),
                        height=dp(24), pos_hint={"center_x": 0.5, "y": 0.02})
        root.add_widget(footer)
        self.add_widget(root)

    def go_to_menu(self):
        self.manager.transition = SlideTransition(direction="left", duration=0.28)
        self.manager.current = "menu"


# ============================================================
#  ECRAN MENU
# ============================================================

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        root.add_widget(GradientBackground(color_top=BG_DARK_1, color_bottom=BG_DARK_2))

        layout = BoxLayout(orientation="vertical", spacing=dp(16), size_hint=(0.86, None),
                            pos_hint={"center_x": 0.5, "center_y": 0.52})
        layout.bind(minimum_height=layout.setter("height"))

        title = Label(text="MENU PRINCIPAL", font_size=dp(24), bold=True, color=TEXT_LIGHT,
                      size_hint=(1, None), height=dp(46))
        layout.add_widget(title)

        routes = {
            "QUIZ": ("quiz_niveaux", ACCENT),
            "REVISION": ("revision", GOLD),
            "EXAMEN": ("examen_niveaux", ACCENT),
            "INFO": ("info", TEXT_MUTED),
            "PARAMETRES": ("parametres", TEXT_MUTED),
        }
        for name, (target, accent) in routes.items():
            row = ListRow(text=name, accent_color=accent, size_hint=(1, None), height=dp(56),
                           on_release=lambda t=target: self.open_section(t))
            layout.add_widget(row)

        back_btn = Card3DButton(text="< RETOUR", bg_color=BG_DARK_1, text_color=TEXT_MUTED,
                                 font_size=dp(14), size_hint=(1, None), height=dp(40),
                                 on_release=self.go_back)
        layout.add_widget(Widget(size_hint=(1, None), height=dp(4)))
        layout.add_widget(back_btn)

        root.add_widget(layout)
        self.add_widget(root)

    def open_section(self, target):
        self.manager.transition = SlideTransition(direction="left", duration=0.24)
        self.manager.current = target

    def go_back(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.28)
        self.manager.current = "welcome"


# ============================================================
#  ECRAN CHOIX DU NIVEAU (Primaire / College / Lycee)
# ============================================================

class QuizNiveauxScreen(Screen):
    CATEGORIES = {
        "PRIMAIRE": NIVEAUX_PRIMAIRE,
        "COLLEGE": NIVEAUX_COLLEGE,
        "LYCEE": NIVEAUX_LYCEE,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        root.add_widget(GradientBackground(color_top=BG_DARK_1, color_bottom=BG_DARK_2))

        container = BoxLayout(orientation="vertical", spacing=dp(12), size_hint=(0.9, None),
                               pos_hint={"center_x": 0.5, "top": 0.96})
        container.bind(minimum_height=container.setter("height"))
        container.add_widget(make_header("Quiz", self.go_back))

        self.tab_bar = TabBar(tabs=list(self.CATEGORIES.keys()), on_select=self.switch_category)
        container.add_widget(self.tab_bar)

        self.scroll = ScrollView(size_hint=(1, None), height=dp(400))
        self.list_layout = BoxLayout(orientation="vertical", spacing=dp(10), size_hint=(1, None))
        self.list_layout.bind(minimum_height=self.list_layout.setter("height"))
        self.scroll.add_widget(self.list_layout)
                container.add_widget(self.scroll)

        root.add_widget(container)
        self.add_widget(root)

        self.current_category = "PRIMAIRE"
        self.build_list()

    def switch_category(self, index, label):
        self.current_category = label
        self.build_list()

    def build_list(self):
        self.list_layout.clear_widgets()
        niveaux = self.CATEGORIES[self.current_category]
        for niveau in niveaux:
            row = ListRow(text=niveau, right_text=">", accent_color=ACCENT,
                           size_hint=(1, None), height=dp(52),
                           on_release=lambda n=niveau: self.select_niveau(n))
            self.list_layout.add_widget(row)

    def select_niveau(self, niveau):
        if self.current_category == "LYCEE":
            serie_screen = self.manager.get_screen("quiz_series")
            serie_screen.set_niveau(niveau)
            self.manager.transition = SlideTransition(direction="left", duration=0.22)
            self.manager.current = "quiz_series"
        else:
            categorie_label = "Primaire" if self.current_category == "PRIMAIRE" else "College"
            matieres = PRIMAIRE_MATIERES if self.current_category == "PRIMAIRE" else COLLEGE_MATIERES
            matieres_screen = self.manager.get_screen("quiz_matieres")
            matieres_screen.set_context(
                niveau=niveau, matieres=matieres,
                titre_niveau="{} {}".format(categorie_label, niveau),
                back_target="quiz_niveaux")
            self.manager.transition = SlideTransition(direction="left", duration=0.22)
            self.manager.current = "quiz_matieres"

    def on_pre_enter(self, *args):
        self.current_category = "PRIMAIRE"
        self.tab_bar.select(0)
        self.build_list()

    def go_back(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.24)
        self.manager.current = "menu"


# ============================================================
#  ECRAN CHOIX DE LA SERIE (SM / SS / SE) POUR LE LYCEE
# ============================================================

class QuizSerieScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.niveau = ""
        root = FloatLayout()
        root.add_widget(GradientBackground(color_top=BG_DARK_1, color_bottom=BG_DARK_2))

        container = BoxLayout(orientation="vertical", spacing=dp(16), size_hint=(0.86, None),
                               pos_hint={"center_x": 0.5, "center_y": 0.52})
        container.bind(minimum_height=container.setter("height"))

        self.header = make_header("Lycee", self.go_back)
        container.add_widget(self.header)

        info = Label(text="Choisis ta serie :", font_size=dp(15), color=TEXT_MUTED,
                     size_hint=(1, None), height=dp(28))
        container.add_widget(info)

        self.tab_bar = TabBar(tabs=SERIES_LYCEE, on_select=self.select_serie, active_index=-1)
        container.add_widget(self.tab_bar)

        root.add_widget(container)
        self.add_widget(root)

    def set_niveau(self, niveau):
        self.niveau = niveau
        self.header.title_label.text = "Lycee - {}".format(niveau)
        for btn in self.tab_bar.buttons:
            btn.set_bg_color(CARD_BG)

    def select_serie(self, index, serie):
        matieres = LYCEE_SS_MATIERES if serie == "SS" else LYCEE_SM_SE_MATIERES
        niveau_key = "{} ({})".format(self.niveau, serie)
        matieres_screen = self.manager.get_screen("quiz_matieres")
        matieres_screen.set_context(
            niveau=niveau_key, matieres=matieres,
            titre_niveau="Lycee {} - {}".format(self.niveau, serie),
            back_target="quiz_series")
        self.manager.transition = SlideTransition(direction="left", duration=0.22)
        self.manager.current = "quiz_matieres"

    def go_back(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.24)
        self.manager.current = "quiz_niveaux"


class QuizMatieresScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.niveau = ""
        self.matieres = []
        self.back_target = "quiz_niveaux"

        root = FloatLayout()
        root.add_widget(GradientBackground(color_top=BG_DARK_1, color_bottom=BG_DARK_2))

        container = BoxLayout(orientation="vertical", spacing=dp(10), size_hint=(0.9, None),
                               pos_hint={"center_x": 0.5, "top": 0.96})
        container.bind(minimum_height=container.setter("height"))

        self.header = make_header("Matieres", self.go_back)
        container.add_widget(self.header)

        self.scroll = ScrollView(size_hint=(1, None), height=dp(430))
        self.list_layout = BoxLayout(orientation="vertical", spacing=dp(10), size_hint=(1, None))
        self.list_layout.bind(minimum_height=self.list_layout.setter("height"))
        self.scroll.add_widget(self.list_layout)
        container.add_widget(self.scroll)

        root.add_widget(container)
        self.add_widget(root)

    def set_context(self, niveau, matieres, titre_niveau, back_target="quiz_niveaux"):
        self.niveau = niveau
        self.matieres = matieres
        self.back_target = back_target
        self.header.title_label.text = titre_niveau
        self.list_layout.clear_widgets()
        for matiere in matieres:
            row = ListRow(text=matiere, right_text=">", accent_color=GOLD,
                           size_hint=(1, None), height=dp(52),
                           on_release=lambda m=matiere: self.select_matiere(m))
            self.list_layout.add_widget(row)

    def select_matiere(self, matiere):
        quiz_screen = self.manager.get_screen("quiz")
        titre = "{} - {}".format(self.header.title_label.text, matiere)
        quiz_screen.set_context(self.niveau, matiere, titre)
        # La flèche du quiz revient toujours à l'écran précédent
        # (liste des matières), et non directement au menu principal.
        quiz_screen.back_screen = self.name
        self.manager.transition = SlideTransition(direction="left", duration=0.22)
        self.manager.current = "quiz"

    def go_back(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.24)
        self.manager.current = self.back_target


# ============================================================
#  ECRAN CHOIX DE LA CLASSE POUR L EXAMEN
# ============================================================

# -----------------------------------------------------------------
# Génération des classements IA
# -----------------------------------------------------------------
def build_ai_ranking(score, total, count, seed_offset=0):
    """Crée un classement simulé avec des candidats IA nommés."""
    rng = random.Random(20260819 + seed_offset + score * 97 + total * 13 + count)
    candidates = []
    names = IA_CANDIDATE_NAMES[:count]
    for name in names:
        # Distribution réaliste : la majorité des scores se situe au milieu/haut.
        ai_score = int(round(rng.triangular(0, total, total * 0.68))) if total else 0
        candidates.append({"name": name, "score": ai_score, "ia": True})
    candidates.append({"name": "PEPE JUSTIN KOLIE", "score": score, "ia": False})
    candidates.sort(key=lambda item: item["score"], reverse=True)
    rank = 1
    for i, candidate in enumerate(candidates):
        if i > 0 and candidate["score"] < candidates[i - 1]["score"]:
            rank = i + 1
        candidate["rank"] = rank
    me = next(c for c in candidates if not c["ia"])
    return {
        "count": count,
        "rank": me["rank"],
        "score": score,
        "total": total,
        "candidates": candidates,
    }


def make_nearby_rows(ranking, max_rows=8):
    candidates = ranking["candidates"]
    my_rank = ranking["rank"]
    start = max(0, my_rank - 3)
    end = min(len(candidates), start + max_rows)
    start = max(0, end - max_rows)
    return candidates[start:end]


def build_candidate_correction(candidate, questions):
    """Construit une copie simulée déterministe pour un candidat du classement."""
    if not questions:
        return []
    total = len(questions)
    score = max(0, min(int(candidate.get("score", 0)), total))
    seed = sum(ord(c) for c in candidate.get("name", "")) + score * 997 + total * 31
    rng = random.Random(seed)
    correct_indices = set(rng.sample(range(total), score)) if score else set()
    corrections = []
    for i, q in enumerate(questions):
        options = list(q.get("options", []))
        correct_idx = int(q.get("answer", 0)) if options else 0
        if i in correct_indices and options:
            selected = options[correct_idx]
            ok = True
        elif options:
            wrong_choices = [j for j in range(len(options)) if j != correct_idx]
            selected = options[rng.choice(wrong_choices)] if wrong_choices else options[correct_idx]
            ok = False
        else:
            selected = ""
            ok = False
        corrections.append({
            "number": i + 1,
            "matiere": q.get("matiere", ""),
            "question": q.get("question", ""),
            "selected": selected,
            "correct": options[correct_idx] if options else "",
            "is_correct": ok,
        })
    return corrections



class ExamenNiveauxScreen(Screen):
    CATEGORIES = {
        "PRIMAIRE": NIVEAUX_PRIMAIRE,
        "COLLEGE": NIVEAUX_COLLEGE,
        "LYCEE": NIVEAUX_LYCEE,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        root.add_widget(GradientBackground(color_top=BG_DARK_1, color_bottom=BG_DARK_2))
        container = BoxLayout(orientation="vertical", spacing=dp(12), size_hint=(0.9, None),
                               pos_hint={"center_x": 0.5, "top": 0.96})
        container.bind(minimum_height=container.setter("height"))
        container.add_widget(make_header("Examen", self.go_back))
        intro = Label(text="Choisis ta classe. L examen couvrira automatiquement toutes les matieres.",
                      color=TEXT_MUTED, font_size=dp(14), halign="center", valign="middle",
                      size_hint=(1, None), height=dp(55))
        intro.bind(size=lambda w,s: setattr(w,"text_size",s))
        container.add_widget(intro)
        self.tab_bar = TabBar(tabs=list(self.CATEGORIES.keys()), on_select=self.switch_category)
        container.add_widget(self.tab_bar)
        self.scroll = ScrollView(size_hint=(1, None), height=dp(410))
        self.list_layout = BoxLayout(orientation="vertical", spacing=dp(10), size_hint=(1,None))
        self.list_layout.bind(minimum_height=self.list_layout.setter("height"))
        self.scroll.add_widget(self.list_layout)
        container.add_widget(self.scroll)
        root.add_widget(container)
        self.add_widget(root)
        self.current_category = "PRIMAIRE"
        self.build_list()

    def switch_category(self, index, label):
        self.current_category = label
        self.build_list()

    def build_list(self):
        self.list_layout.clear_widgets()
        for niveau in self.CATEGORIES[self.current_category]:
            row = ListRow(text=niveau, right_text="DEMARRER >", accent_color=GOLD,
                          size_hint=(1,None), height=dp(54),
                          on_release=lambda n=niveau: self.select_niveau(n))
            self.list_layout.add_widget(row)

    def select_niveau(self, niveau):
        if self.current_category == "LYCEE":
            screen = self.manager.get_screen("examen_series")
            screen.set_niveau(niveau)
            self.manager.transition = SlideTransition(direction="left", duration=0.22)
            self.manager.current = "examen_series"
        else:
            matieres = PRIMAIRE_MATIERES if self.current_category == "PRIMAIRE" else COLLEGE_MATIERES
            self.start_exam(niveau, matieres)

    def start_exam(self, niveau, matieres):
        exam = self.manager.get_screen("examen")
        exam.set_exam_context(niveau, matieres, "Examen - {}".format(niveau))
        self.manager.transition = SlideTransition(direction="left", duration=0.22)
        self.manager.current = "examen"

    def go_back(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.24)
        self.manager.current = "menu"


class ExamenSerieScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.niveau = ""
        root = FloatLayout()
        root.add_widget(GradientBackground(color_top=BG_DARK_1, color_bottom=BG_DARK_2))
        container = BoxLayout(orientation="vertical", spacing=dp(16), size_hint=(0.86,None),
                               pos_hint={"center_x":0.5,"center_y":0.52})
        container.bind(minimum_height=container.setter("height"))
        self.header = make_header("Examen - Lycee", self.go_back)
        container.add_widget(self.header)
        info = Label(text="Choisis ta serie pour determiner toutes les matieres de l examen.",
                             color=TEXT_MUTED, font_size=dp(14), halign="center", valign="middle",
                     size_hint=(1,None), height=dp(55))
        info.bind(size=lambda w,s:setattr(w,"text_size",s))
        container.add_widget(info)
        self.tab_bar = TabBar(tabs=SERIES_LYCEE, on_select=self.select_serie, active_index=-1)
        container.add_widget(self.tab_bar)
        root.add_widget(container)
        self.add_widget(root)

    def set_niveau(self, niveau):
        self.niveau = niveau
        self.header.title_label.text = "Examen - {}".format(niveau)
        for btn in self.tab_bar.buttons:
            btn.set_bg_color(CARD_BG)

    def select_serie(self, index, serie):
        matieres = LYCEE_SS_MATIERES if serie == "SS" else LYCEE_SM_SE_MATIERES
        niveau_key = "{} ({})".format(self.niveau, serie)
        exam = self.manager.get_screen("examen")
        exam.set_exam_context(niveau_key, matieres, "Examen - {}".format(niveau_key))
        self.manager.transition = SlideTransition(direction="left", duration=0.22)
        self.manager.current = "examen"

    def go_back(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.24)
        self.manager.current = "examen_niveaux"


# ============================================================
#  ECRAN QUIZ / EXAMEN (moteur commun)
# ============================================================

class QuizEngineScreen(Screen):
    """Ecran generique de questions, utilise pour le Quiz et l'Examen."""

    def __init__(self, questions=None, exam_mode=False, time_limit=None,
                 title="Quiz", **kwargs):
        super().__init__(**kwargs)
        self.static_questions = questions
        self.dynamic = questions is None
        self.exam_dynamic = exam_mode and questions is None
        self.exam_matieres = []
        self.niveau = None
        self.matiere = None
        self.questions = questions or []
        self.exam_mode = exam_mode
        self.time_limit = time_limit
        self.title_text = title
        # Écran à retrouver avec la flèche retour.
        self.back_screen = "menu"

        self.index = 0
        self.score = 0
        self.exam_corrections = []
        self.current_shuffled_options = []
        self.current_question_number = 0
        self.answered = False
        self.remaining = time_limit or 0
        self._timer_event = None
        self._next_event = None

        self.root_layout = FloatLayout()
        self.root_layout.add_widget(GradientBackground(color_top=BG_DARK_1, color_bottom=BG_DARK_2))

        self.container = BoxLayout(orientation="vertical", spacing=dp(14), size_hint=(0.9, None),
                                    pos_hint={"center_x": 0.5, "top": 0.96})
        self.container.bind(minimum_height=self.container.setter("height"))

        self.header = make_header(title, self.confirm_leave)
        self.container.add_widget(self.header)

        info_row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(26))
        self.progress_label = Label(text="", color=TEXT_MUTED, font_size=dp(13), halign="left", valign="middle")
        self.progress_label.bind(size=lambda w, s: setattr(w, "text_size", s))
        self.timer_label = Label(text="", color=GOLD, font_size=dp(13), bold=True, halign="right", valign="middle")
        self.timer_label.bind(size=lambda w, s: setattr(w, "text_size", s))
        info_row.add_widget(self.progress_label)
        info_row.add_widget(self.timer_label)
        self.container.add_widget(info_row)

        self.question_label = Label(text="", color=TEXT_LIGHT, font_size=dp(18), bold=True,
                                     halign="left", valign="middle", size_hint=(1, None), height=dp(90))
        self.question_label.bind(size=lambda w, s: setattr(w, "text_size", s))
        self.container.add_widget(self.question_label)

        self.answers_box = BoxLayout(orientation="vertical", spacing=dp(10), size_hint=(1, None))
        self.answers_box.bind(minimum_height=self.answers_box.setter("height"))
        self.container.add_widget(self.answers_box)

        self.feedback_label = Label(text="", font_size=dp(14), bold=True, size_hint=(1, None), height=dp(28))
        self.container.add_widget(self.feedback_label)

        self.next_btn = Card3DButton(text="SUIVANT", bg_color=ACCENT, text_color=TEXT_LIGHT,
                                      font_size=dp(16), size_hint=(1, None), height=dp(48),
                                      on_release=self.next_question)
        if not self.exam_mode:
            self.container.add_widget(self.next_btn)

        self.root_layout.add_widget(self.container)
        self.add_widget(self.root_layout)

    # ----- cycle de vie -----
    def set_context(self, niveau, matiere, titre):
        self.niveau = niveau
        self.matiere = matiere
        self.title_text = titre
        self.header.title_label.text = titre

    def set_exam_context(self, niveau, matieres, titre):
        self.niveau = niveau
        self.exam_matieres = list(matieres)
        self.matiere = None
        self.title_text = titre
        self.exam_dynamic = True
        self.header.title_label.text = titre

    def on_pre_enter(self, *args):
        self.reset()

    def on_leave(self, *args):
        self._stop_timer()
        self._cancel_next_event()

    def confirm_leave(self):
        self._stop_timer()
        self._cancel_next_event()
        self.manager.transition = SlideTransition(direction="right", duration=0.24)
        # Retour d'un seul niveau : Quiz -> Matières -> Série/Niveaux.
        self.manager.current = self.back_screen

    # ----- logique du quiz -----
    def reset(self):
        self._stop_timer()
        self._cancel_next_event()
        self.index = 0
        self.score = 0
        self.exam_corrections = []
        self.current_shuffled_options = []
        self.current_question_number = 0
        self.answered = False

        if self.exam_mode and self.exam_dynamic:
            self.questions = get_exam_questions(self.niveau, self.exam_matieres, QUESTIONS_PAR_MATIERE_EXAMEN) \
                if self.niveau and self.exam_matieres else []
        elif self.dynamic:
            self.questions = get_questions(self.niveau, self.matiere, QUESTIONS_PAR_QUIZ) \
                if self.niveau and self.matiere else []
        else:
            self.questions = self.static_questions

        if not self.questions:
            self._show_unavailable()
            return

        self.timer_label.text = ""
        self.build_question()

    def _show_unavailable(self):
        self.progress_label.text = ""
        self.question_label.text = "Cette matiere sera bientot disponible."
        self.answers_box.clear_widgets()
        self.feedback_label.text = ""
        self.next_btn.opacity = 0
        self.next_btn.disabled = True

    def build_question(self):
        q = self.questions[self.index]
        if self.exam_mode and q.get("matiere"):
            self.progress_label.text = "Question {}/{} • {}".format(self.index + 1, len(self.questions), q.get("matiere"))
        else:
            self.progress_label.text = "Question {}/{}".format(self.index + 1, len(self.questions))
        self.question_label.text = q["question"]
        if self.exam_mode:
            self.remaining = self.time_limit
            self._start_timer()
        self.feedback_label.text = ""
        self.answered = False
        self.next_btn.opacity = 0.4
        self.next_btn.disabled = True

        # Melange les choix a chaque question. L'index de la bonne reponse
        # est recalcule apres le melange afin qu'elle ne soit pas toujours A.
        indexed_options = list(enumerate(q["options"]))
        random.shuffle(indexed_options)
        self.current_correct_idx = next(
            i for i, (old_i, _) in enumerate(indexed_options)
            if old_i == q["answer"]
        )
        self.current_shuffled_options = [opt for _, opt in indexed_options]
        self.current_question_number = self.index + 1

        self.answers_box.clear_widgets()
        for i, (_, opt) in enumerate(indexed_options):
            row = AnswerOptionRow(text=opt, index=i, on_select=self.select_answer,
                                   size_hint=(1, None), height=dp(50))
            self.answers_box.add_widget(row)

    def select_answer(self, idx, row):
        if self.answered:
            return
        self.answered = True
        if self.exam_mode:
            self._stop_timer()
        q = self.questions[self.index]
        correct_idx = self.current_correct_idx
        for r in self.answers_box.children:
            if r.index == correct_idx:
                r.set_state("correct")
            elif r.index == idx:
                r.set_state("wrong")
            else:
                r.locked = True

        selected_text = self.current_shuffled_options[idx] if 0 <= idx < len(self.current_shuffled_options) else ""
        correct_text = q["options"][q["answer"]]
        self.exam_corrections.append({
            "number": self.current_question_number,
            "matiere": q.get("matiere", ""),
            "question": q["question"],
            "selected": selected_text,
            "correct": correct_text,
            "is_correct": idx == correct_idx,
        })

        if idx == correct_idx:
            self.score += 1
            self.feedback_label.text = "Bonne reponse !"
            self.feedback_label.color = GREEN
        else:
            self.feedback_label.text = "Reponse incorrecte."
            self.feedback_label.color = RED

        # Passage automatique a la question suivante pour le Quiz ET l'Examen.
        # Un court delai permet de voir la correction avant de continuer.
        self.next_btn.opacity = 0
        self.next_btn.disabled = True
        self._cancel_next_event()
        self._next_event = Clock.schedule_once(lambda dt: self.next_question(), 0.65)

    def _time_expired(self):
        if self.answered:
            return
        self.answered = True
        for r in self.answers_box.children:
            r.locked = True
        q = self.questions[self.index]
        self.exam_corrections.append({
            "number": self.current_question_number,
            "matiere": q.get("matiere", ""),
            "question": q["question"],
            "selected": "Aucune réponse (temps écoulé)",
            "correct": q["options"][q["answer"]],
            "is_correct": False,
        })
        self.feedback_label.text = "Temps ecoule !"
        self.feedback_label.color = RED
        self._stop_timer()
        self._cancel_next_event()
        self._next_event = Clock.schedule_once(lambda dt: self.next_question(), 0.35)

    def _cancel_next_event(self):
        if self._next_event is not None:
            try:
                self._next_event.cancel()
            except Exception:
                pass
            self._next_event = None

    def next_question(self, *args):
        if not self.answered:
            return
        self.index += 1
        if self.index >= len(self.questions):
            self.finish()
        else:
            self.build_question()

    def finish(self):
        self._stop_timer()
        self._cancel_next_event()
        if self.score > BEST_SCORES.get(self.name, 0):
            BEST_SCORES[self.name] = self.score

        if self.exam_mode:
            # Fin de l examen : les copies passent d abord par une phase de
            # correction/publication. Les résultats ne sont donc pas immédiats.
            LAST_EXAM_RESULT.clear()
            LAST_EXAM_RESULT.update({
                "title": self.title_text,
                "score": self.score,
                "total": len(self.questions),
                "niveau": self.niveau or "Classe",
                "corrections": list(self.exam_corrections),
                "questions": [dict(q) for q in self.questions],
            })
            # Passage sécurisé vers l'écran de correction. Si, pour une
            # raison quelconque, l'écran n'est pas disponible, on affiche
            # immédiatement le résultat au lieu de laisser l'application
            # provoquer une exception et se fermer.
            try:
                correction = self.manager.get_screen("examen_correction")
                correction.prepare(dict(LAST_EXAM_RESULT))
                self.manager.transition = FadeTransition(duration=0.25)
                self.manager.current = "examen_correction"
            except Exception:
                result_screen = self.manager.get_screen("resultat")
                result_screen.publish_exam(
                    self.title_text, self.score, len(self.questions),
                    self.niveau or "Classe"
                )
                self.manager.transition = FadeTransition(duration=0.25)
                self.manager.current = "resultat"
            return

        result_screen = self.manager.get_screen("resultat")
        result_screen.set_result(self.title_text, self.score, len(self.questions), self.name)
        self.manager.transition = FadeTransition(duration=0.25)
        self.manager.current = "resultat"

    # ----- minuteur (mode examen) -----
    def _start_timer(self):
        self._update_timer_label()
        self._timer_event = Clock.schedule_interval(self._tick, 1)

    def _stop_timer(self):
        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None

    def _tick(self, dt):
        self.remaining -= 1
        self._update_timer_label()
        if self.remaining <= 0:
            if self.exam_mode:
                self._time_expired()
            else:
                self.finish()

    def _update_timer_label(self):
        m, s = divmod(max(self.remaining, 0), 60)
        self.timer_label.text = "{:02d}:{:02d}".format(m, s)


# ============================================================
#  ECRAN INTRO EXAMEN
# ============================================================

class ExamenIntroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        root.add_widget(GradientBackground(color_top=BG_DARK_1, color_bottom=BG_DARK_2))

        container = BoxLayout(orientation="vertical", spacing=dp(16), size_hint=(0.86, None),
                               pos_hint={"center_x": 0.5, "center_y": 0.52})
        container.bind(minimum_height=container.setter("height"))

        container.add_widget(make_header("Examen", self.go_back))

        icon = Label(text="EXAMEN", font_size=dp(30), bold=True, color=GOLD,
                     size_hint=(1, None), height=dp(50))
        desc = Label(
            text=("{} questions - {} secondes.\n"
                  "Chaque question passe automatiquement une fois repondue.\n"
                  "Pret(e) a commencer ?").format(len(QUESTIONS_EXAMEN), EXAMEN_DUREE_SEC),
            font_size=dp(15), color=TEXT_MUTED, halign="center", valign="middle",
            size_hint=(1, None), height=dp(90))
        desc.bind(size=lambda w, s: setattr(w, "text_size", s))

        start_btn = Card3DButton(text="COMMENCER", bg_color=ACCENT, text_color=TEXT_LIGHT,
        
    def _exam_questions_for_detail(self):
        # Les questions de l'examen courant sont conservées dans LAST_EXAM_RESULT.
        return LAST_EXAM_RESULT.get("questions", [])

    def retry(self):
        target_screen = self.manager.get_screen(self.source_name)
        target_screen.reset()
        self.manager.transition = FadeTransition(duration=0.2)
        self.manager.current = self.source_name

    def go_menu(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.24)
        self.manager.current = "menu"

# ============================================================
#  ECRAN REVISION
# ============================================================

class RevisionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        root.add_widget(GradientBackground(color_top=BG_DARK_1, color_bottom=BG_DARK_2))

        container = BoxLayout(orientation="vertical", spacing=dp(10), size_hint=(0.9, None),
                               pos_hint={"center_x": 0.5, "top": 0.96})
        container.bind(minimum_height=container.setter("height"))
        container.add_widget(make_header("Revision", self.go_back))

        hint = Label(text="Touche une fiche pour reveler la reponse.", font_size=dp(13),
                     color=TEXT_MUTED, size_hint=(1, None), height=dp(24))
        container.add_widget(hint)

        scroll = ScrollView(size_hint=(1, None), height=dp(430))
        cards_layout = BoxLayout(orientation="vertical", spacing=dp(10), size_hint=(1, None))
        cards_layout.bind(minimum_height=cards_layout.setter("height"))

        for card in REVISION_CARDS:
            row = FlashcardRow(question=card["question"], answer=card["answer"],
                                size_hint=(1, None), height=dp(64))
            cards_layout.add_widget(row)

        scroll.add_widget(cards_layout)
        container.add_widget(scroll)
        root.add_widget(container)
        self.add_widget(root)

    def go_back(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.24)
        self.manager.current = "menu"


# ============================================================
#  ECRAN INFO
# ============================================================

class InfoDetailScreen(Screen):
    """Page DETAIL : une seule rubrique est affichee a la fois."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        root.add_widget(GradientBackground(color_top=BG_DARK_1, color_bottom=BG_DARK_2))

        # Toute la page detail est independante de la page INFO.
        container = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=(dp(10), dp(10)),
            size_hint=(0.92, 0.90),
            pos_hint={"center_x": 0.5, "center_y": 0.50},
        )

        self.header = make_header("Informations", self.go_back)
        container.add_widget(self.header)

        # Carte blanche/dark qui contient UNIQUEMENT le texte de la rubrique.
        card = BoxLayout(
            orientation="vertical",
            padding=(dp(16), dp(16)),
            size_hint=(1, 1),
        )
        with card.canvas.before:
            Color(*CARD_BG)
            self.card_bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(16)])
        card.bind(pos=self._update_card, size=self._update_card)

        scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(5),
        )

        self.text_label = Label(
            text="",
            font_size=dp(16),
            color=TEXT_LIGHT,
            halign="left",
            valign="top",
            size_hint=(1, None),
            padding=(dp(4), dp(4)),
        )
        self.text_label.bind(width=self._update_text_width)
        self.text_label.bind(texture_size=self._update_text_height)

        scroll.add_widget(self.text_label)
        card.add_widget(scroll)
        container.add_widget(card)
        root.add_widget(container)
        self.add_widget(root)

    def _update_card(self, instance, *args):
        self.card_bg.pos = instance.pos
        self.card_bg.size = instance.size

    def _update_text_width(self, instance, width):
        instance.text_size = (max(width - dp(8), dp(100)), None)
        instance.texture_update()
        instance.height = max(instance.texture_size[1] + dp(20), dp(200))

    def _update_text_height(self, instance, texture_size):
        instance.height = max(texture_size[1] + dp(20), dp(200))

    def show_section(self, section):
        infos = {
            "app": (
                "À PROPOS DE KOLIÉ QUIZ\n\n"
                "KOLIÉ QUIZ est une application éducative conçue pour aider les élèves à réviser, à s'entraîner et à améliorer leurs connaissances.\n\n"
                "OBJECTIF\n\n"
                "Créer une plateforme simple, moderne et interactive permettant aux élèves de travailler régulièrement dans plusieurs matières.\n\n"
                "ESPACES DE L'APPLICATION\n\n"
                "• QUIZ : entraînement avec questions à choix multiples.\n"
                "• RÉVISION : fiches pour revoir les notions.\n"
                "• EXAMEN : mode d'évaluation avec temps limité.\n"
                "• RÉSULTATS : affichage du score obtenu.\n"
                "• INFO : présentation du projet et de son développeur.\n"
                "• PARAMÈTRES : gestion des options de l'application.\n\n"
                "Le Quiz utilise actuellement le niveau INTERMÉDIAIRE pour toutes les classes."
            ),
            "quiz": (
                "FONCTIONNEMENT DU QUIZ\n\n"
                "1. L'utilisateur choisit sa classe.\n"
                "2. Il choisit, lorsque nécessaire, sa série.\n"
                "3. Il choisit une matière.\n"
                "4. Le Quiz prépare un nouveau lot de questions.\n\n"
                "NIVEAU\n\n"
                "Toutes les classes utilisent le niveau INTERMÉDIAIRE.\n\n"
                "QUESTIONS\n\n"
                "Chaque session contient 20 questions. Les questions sont tirées de la banque correspondant au niveau et à la matière.\n\n"
                "ANTI-RÉPÉTITION\n\n"
                "Les questions déjà utilisées sont mémorisées. Lorsqu'un Quiz est terminé ou lorsque l'utilisateur quitte l'écran du Quiz, le prochain Quiz sélectionne un nouveau lot afin d'éviter de reprendre les questions précédentes tant que la banque contient suffisamment de questions.\n\n"
                "RÉPONSE AUTOMATIQUE\n\n"
                "Dès que l'utilisateur appuie sur une réponse, celle-ci est corrigée. Après un court délai, la question suivante s'affiche automatiquement. Il n'est donc pas nécessaire d'appuyer sur un bouton SUIVANT.\n\n"
                "À la fin du Quiz, le score est calculé et présenté dans l'écran des résultats."
            ),
            "classes": (
                "CLASSES ET NIVEAUX\n\n"
                "PRIMAIRE\n\n"
                "1ère A\n2ème A\n3ème A\n4ème A\n5ème A\n6ème A\n\n"
                "COLLÈGE\n\n"
                "7ème A\n8ème A\n9ème A\n10ème A\n\n"
                "LYCÉE\n\n"
                "11ème A\n12ème A\nTerminale A\n\n"
                "SÉRIES\n\n"
                "Selon la classe, les séries et les matières correspondantes sont proposées dans l'application.\n\n"
                "DIFFICULTÉ\n\n"
                "Le niveau du Quiz est INTERMÉDIAIRE pour toutes les classes."
            ),
            "dev": (
                "DÉVELOPPEUR\n\n"
                "PEPE JUSTIN KOLIE\n\n"
                "IDENTITÉ DU PROJET\n\n"
                "Nom : PEPE JUSTIN KOLIE\n"
                "Rôle : concepteur et développeur\n"
                "Projet : KOLIÉ QUIZ\n"
                "Version actuelle : 1.0.0\n\n"
                "TECHNOLOGIES\n\n"
                "• Python\n"
                "• Kivy\n"
                "• Pydroid3\n"
                "• Plateforme cible : Android\n\n"
                "TRAVAIL RÉALISÉ\n\n"
                "Conception de l'interface, organisation des écrans, création du moteur de Quiz, gestion des questions, sélection des classes et matières, calcul des scores, résultats, révision, examen et paramètres.\n\n"
                "FONCTIONNALITÉS DU PROJET\n\n"
                "• Questions à choix multiples\n"
                "• Niveau intermédiaire pour toutes les classes\n"
                "• Renouvellement des questions entre les sessions\n"
                "• Passage automatique à la question suivante\n"
                "• Système de résultats et de scores\n"
                "• Mode examen\n"
                "• Espace révision\n"
                "• Interface adaptée à Android\n\n"
                "VISION\n\n"
                "Faire évoluer KOLIÉ QUIZ vers une plateforme éducative complète permettant aux élèves de s'exercer régulièrement, de suivre leurs progrès et de mieux préparer leurs évaluations scolaires.\n\n"
                "CRÉDITS\n\n"
                "Conception et développement : PEPE JUSTIN KOLIE.\n\n"
                "KOLIÉ QUIZ est un projet éducatif destiné à l'apprentissage et à l'entraînement scolaire."
            ),
        }
        titles = {
            "app": "À propos de KOLIÉ QUIZ",
            "quiz": "Fonctionnement du Quiz",
            "classes": "Classes et niveaux",
            "dev": "Développeur",
        }

        self.header.title_label.text = titles.get(section, "Informations")
        self.text_label.text = infos.get(section, "Aucune information disponible.")
        self.text_label.texture_update()
        self._update_text_width(self.text_label, self.text_label.width)

    def go_back(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.24)
        self.manager.current = "info"


class InfoScreen(Screen):
    """Menu INFO : chaque rubrique est un bouton ouvrant une page de contenu."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        root.add_widget(GradientBackground(color_top=BG_DARK_1, color_bottom=BG_DARK_2))

        container = BoxLayout(orientation="vertical", spacing=dp(10),
                              size_hint=(0.90, 0.88),
                              pos_hint={"center_x": 0.5, "center_y": 0.50})
        container.add_widget(make_header("Info", self.go_back))

        intro = Label(text="INFORMATIONS DE KOLIÉ QUIZ\nChoisissez une rubrique pour ouvrir son contenu.",
                      font_size=dp(15), color=TEXT_MUTED, halign="center", valign="middle",
                      size_hint=(1, None), height=dp(65))
        intro.bind(size=lambda w, s: setattr(w, "text_size", s))
        container.add_widget(intro)

        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        content = BoxLayout(orientation="vertical", spacing=dp(10), size_hint=(1, None),
                            padding=(0, dp(5)))
        content.bind(minimum_height=content.setter("height"))

        buttons = [
            ("À propos de KOLIÉ QUIZ", "app", ACCENT),
            ("Fonctionnement du Quiz", "quiz", GOLD),
            ("Classes et niveaux", "classes", GREEN),
            ("Développeur : PEPE JUSTIN KOLIE", "dev", GOLD),
        ]
        for text, section, accent in buttons:
            btn = ListRow(text=text, right_text="OUVRIR >", accent_color=accent,
                          interactive=True,
                          on_release=lambda sec=section: self.open_section(sec),
                          size_hint=(1, None), height=dp(58))
            content.add_widget(btn)

        # Informations générales non interactives
        content.add_widget(ListRow(text="Version", right_text="1.0.0", accent_color=TEXT_MUTED,
                                    interactive=False, size_hint=(1, None), height=dp(46)))
        self.row_best_quiz = ListRow(text="Meilleur score Quiz", right_text="0", accent_color=GOLD,
                                     interactive=False, size_hint=(1, None), height=dp(46))
        self.row_best_examen = ListRow(text="Meilleur score Examen", right_text="0", accent_color=GOLD,
                                       interactive=False, size_hint=(1, None), height=dp(46))
        content.add_widget(self.row_best_quiz)
        content.add_widget(self.row_best_examen)

        scroll.add_widget(content)
        container.add_widget(scroll)
        root.add_widget(container)
        self.add_widget(root)

    def open_section(self, section):
        detail = self.manager.get_screen("info_detail")
        detail.show_section(section)
        self.manager.transition = SlideTransition(direction="left", duration=0.24)
        self.manager.current = "info_detail"

    def on_pre_enter(self, *args):
        self.row_best_quiz.set_right_text(str(BEST_SCORES.get("quiz", 0)))
        self.row_best_examen.set_right_text(str(BEST_SCORES.get("examen", 0)))

    def go_back(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.24)
        self.manager.current = "menu"


# ============================================================
#  ECRAN PARAMETRES
# ============================================================

class ParametresScreen(Screen):
    DIFFICULTES = ["Intermediaire"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        root.add_widget(GradientBackground(color_top=BG_DARK_1, color_bottom=BG_DARK_2))

        container = BoxLayout(orientation="vertical", spacing=dp(12), size_hint=(0.86, None),
                               pos_hint={"center_x": 0.5, "top": 0.96})
        container.bind(minimum_height=container.setter("height"))
        container.add_widget(make_header("Parametres", self.go_back))

        self.row_son = ListRow(text="Son", right_text=self._son_text(), accent_color=ACCENT,
                                interactive=True, on_release=self.toggle_son,
                                size_hint=(1, None), height=dp(52))
        self.row_difficulte = ListRow(text="Difficulte", right_text=APP_SETTINGS["difficulte"],
                                       accent_color=GOLD, interactive=True,
                                       on_release=self.cycle_difficulte,
                                       size_hint=(1, None), height=dp(52))
        self.row_reset = ListRow(text="Reinitialiser la progression", right_text=">",
                                  accent_color=RED, interactive=True,
                                  on_release=self.reset_progress,
                                  size_hint=(1, None), height=dp(52))

        container.add_widget(self.row_son)
        container.add_widget(self.row_difficulte)
        container.add_widget(self.row_reset)

        self.status_label = Label(text="", font_size=dp(13), color=GREEN,
                                   size_hint=(1, None), height=dp(24))
        container.add_widget(self.status_label)

        root.add_widget(container)
        self.add_widget(root)

    def _son_text(self):
        return "Active" if APP_SETTINGS["son"] else "Coupe"

    def toggle_son(self):
        APP_SETTINGS["son"] = not APP_SETTINGS["son"]
        self.row_son.set_right_text(self._son_text())
        self.status_label.text = "Son mis a jour."

    def cycle_difficulte(self):
        idx = self.DIFFICULTES.index(APP_SETTINGS["difficulte"])
        APP_SETTINGS["difficulte"] = self.DIFFICULTES[(idx + 1) % len(self.DIFFICULTES)]
        self.row_difficulte.set_right_text(APP_SETTINGS["difficulte"])
        self.status_label.text = "Difficulte mise a jour."

    def reset_progress(self):
        BEST_SCORES["quiz"] = 0
        BEST_SCORES["examen"] = 0
        LAST_EXAM_RESULT.clear()
        self.status_label.text = "Progression reinitialisee !"

    def go_back(self):
        self.manager.transition = SlideTransition(direction="right", duration=0.24)
        self.manager.current = "menu"


# ============================================================
#  APPLICATION
# ============================================================

class QuizKolieApp(App):
    def build(self):
        self.title = "QUIZ KOLIE"
        Window.clearcolor = BG_DARK_1

        sm = ScreenManager(transition=FadeTransition(duration=0.2))
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(QuizNiveauxScreen(name="quiz_niveaux"))
        sm.add_widget(QuizSerieScreen(name="quiz_series"))
        sm.add_widget(QuizMatieresScreen(name="quiz_matieres"))
        sm.add_widget(QuizEngineScreen(questions=None, exam_mode=False,
                                        title="Quiz", name="quiz"))
        sm.add_widget(ExamenIntroScreen(name="examen_intro"))
        sm.add_widget(ExamenNiveauxScreen(name="examen_niveaux"))
        sm.add_widget(ExamenSerieScreen(name="examen_series"))
        sm.add_widget(QuizEngineScreen(questions=None, exam_mode=True,
                                        time_limit=EXAMEN_DUREE_SEC, title="Examen", name="examen"))
        sm.add_widget(ExamenCorrectionScreen(name="examen_correction"))
        sm.add_widget(ExamenCorrectionDetailScreen(name="examen_correction_detail"))
        sm.add_widget(ResultScreen(name="resultat"))
        sm.add_widget(RevisionScreen(name="revision"))
        sm.add_widget(InfoScreen(name="info"))
        sm.add_widget(InfoDetailScreen(name="info_detail"))
        sm.add_widget(ParametresScreen(name="parametres"))
        return sm


if __name__ == "__main__":
    QuizKolieApp().run()
