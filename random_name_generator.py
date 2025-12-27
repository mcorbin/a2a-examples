#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de noms aléatoires français
Ce script génère des noms français complets (prénom + nom de famille)
"""

import random


# Listes de prénoms français courants (masculins et féminins)
PRENOMS_MASCULINS = [
    "Jean", "Pierre", "Michel", "André", "Philippe",
    "Marc", "Alain", "Jacques", "Christian", "François",
    "Patrick", "Daniel", "Bernard", "Thomas", "Robert",
    "Paul", "Luc", "Olivier", "Laurent", "Vincent",
    "Christophe", "Serge", "Georges", "Joseph", "Claude",
    "Stéphane", "Frédéric", "Thierry", "Gérard", "Yves",
    "Maxime", "Lucas", "Hugo", "Nathan", "Louis",
    "Gabriel", "Raphaël", "Léo", "Arthur", "Mathieu"
]

PRENOMS_FEMININS = [
    "Marie", "Anne", "Isabelle", "Nathalie", "Catherine",
    "Christine", "Monique", "Martine", "Jacqueline", "Sylvie",
    "Valérie", "Sandrine", "Dominique", "Véronique", "Chantal",
    "Francine", "Danielle", "Michèle", "Stéphanie", "Laurence",
    "Pascale", "Brigitte", "Cécile", "Corinne", "Muriel",
    "Sophie", "Laure", "Céline", "Virginie", "Mélanie",
    "Émilie", "Camille", "Léa", "Clara", "Zoé",
    "Manon", "Lucie", "Juliette", "Inès", "Amélie"
]

# Listes de noms de famille français courants
NOMS_FAMILLE = [
    "Martin", "Bernard", "Dubois", "Thomas", "Robert",
    "Richard", "Petit", "Durand", "Lefevre", "Moreau",
    "Simon", "Laurent", "Lefebvre", "Michel", "Garcia",
    "David", "Bertrand", "Roux", "Vincent", "Fournier",
    "Morel", "Girardin", "André", "Leroy", "Hubert",
    "Blanc", "Gillet", "Rousseau", "Brun", "Gérard",
    "Boulanger", "Barbier", "Carpentier", "Charpentier", "Chevalier",
    "Collet", "Collin", "Collard", "Colas", "Coste",
    "Coulon", "Coupé", "Courbet", "Courtin", "Cousin",
    "Coutard", "Couturier", "Couzin", "Coyaud", "Coyette",
    "Deschamps", "Desrosiers", "Devereux", "Devos", "Dewolf",
    "Déziel", "Diallo", "Diaz", "Dibble", "Dickens",
    "Diderot", "Didier", "Dieudonné", "Dieu", "Dieudé",
    "Dieulot", "Dieuzaide", "Dieuzayde", "Dieuzé", "Dieuzéa"
]


def generer_nom_aleatoire(genre=None):
    """
    Génère un nom français aléatoire complet.
    
    Args:
        genre (str, optional): 'M' pour masculin, 'F' pour féminin.
                              Si None, le genre est choisi aléatoirement.
    
    Returns:
        str: Un nom complet (prénom + nom de famille)
    
    Exemples:
        >>> nom = generer_nom_aleatoire()
        >>> print(nom)
        'Jean Martin'
        
        >>> nom = generer_nom_aleatoire(genre='F')
        >>> print(nom)
        'Marie Dubois'
    """
    # Déterminer le genre si non spécifié
    if genre is None:
        genre = random.choice(['M', 'F'])
    
    # Sélectionner le prénom selon le genre
    if genre.upper() == 'M':
        prenom = random.choice(PRENOMS_MASCULINS)
    elif genre.upper() == 'F':
        prenom = random.choice(PRENOMS_FEMININS)
    else:
        raise ValueError("Le genre doit être 'M' ou 'F'")
    
    # Sélectionner un nom de famille aléatoire
    nom_famille = random.choice(NOMS_FAMILLE)
    
    # Retourner le nom complet
    return f"{prenom} {nom_famille}"


def generer_plusieurs_noms(nombre, genre=None):
    """
    Génère plusieurs noms français aléatoires.
    
    Args:
        nombre (int): Le nombre de noms à générer
        genre (str, optional): 'M' pour masculin, 'F' pour féminin.
                              Si None, le genre est choisi aléatoirement pour chaque nom.
    
    Returns:
        list: Une liste de noms complets
    
    Exemples:
        >>> noms = generer_plusieurs_noms(5)
        >>> for nom in noms:
        ...     print(nom)
        
        >>> noms = generer_plusieurs_noms(3, genre='F')
        >>> print(noms)
        ['Sophie Martin', 'Laure Dubois', 'Céline Thomas']
    """
    if nombre <= 0:
        raise ValueError("Le nombre de noms doit être positif")
    
    noms = [generer_nom_aleatoire(genre) for _ in range(nombre)]
    return noms


def afficher_noms(noms):
    """
    Affiche une liste de noms de manière formatée.
    
    Args:
        noms (list): Une liste de noms à afficher
    """
    print("\n" + "="*50)
    print("NOMS GÉNÉRÉS")
    print("="*50)
    for i, nom in enumerate(noms, 1):
        print(f"{i:2d}. {nom}")
    print("="*50 + "\n")


# Programme principal
if __name__ == "__main__":
    print("\n🇫🇷 GÉNÉRATEUR DE NOMS ALÉATOIRES FRANÇAIS 🇫🇷\n")
    
    # Exemple 1: Générer un seul nom aléatoire
    print("1️⃣  Un nom aléatoire (genre aléatoire):")
    nom = generer_nom_aleatoire()
    print(f"   → {nom}\n")
    
    # Exemple 2: Générer un nom masculin
    print("2️⃣  Un nom masculin:")
    nom_m = generer_nom_aleatoire(genre='M')
    print(f"   → {nom_m}\n")
    
    # Exemple 3: Générer un nom féminin
    print("3️⃣  Un nom féminin:")
    nom_f = generer_nom_aleatoire(genre='F')
    print(f"   → {nom_f}\n")
    
    # Exemple 4: Générer plusieurs noms
    print("4️⃣  Dix noms aléatoires:")
    noms = generer_plusieurs_noms(10)
    afficher_noms(noms)
    
    # Exemple 5: Générer plusieurs noms féminins
    print("5️⃣  Cinq noms féminins:")
    noms_f = generer_plusieurs_noms(5, genre='F')
    afficher_noms(noms_f)
    
    # Exemple 6: Générer plusieurs noms masculins
    print("6️⃣  Cinq noms masculins:")
    noms_m = generer_plusieurs_noms(5, genre='M')
    afficher_noms(noms_m)
