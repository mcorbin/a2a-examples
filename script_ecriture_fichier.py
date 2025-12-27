#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour écrire l'input utilisateur dans un fichier
Permet d'ajouter du texte à un fichier existant ou de créer un nouveau fichier
"""

import os
import sys


def afficher_menu():
    """Affiche le menu principal"""
    print("\n" + "="*50)
    print("GESTIONNAIRE D'ÉCRITURE DE FICHIER")
    print("="*50)
    print("1. Créer un nouveau fichier (remplacer si existant)")
    print("2. Ajouter du texte à un fichier existant")
    print("3. Quitter")
    print("="*50)


def obtenir_nom_fichier():
    """Demande à l'utilisateur le nom du fichier"""
    while True:
        nom_fichier = input("\nEntrez le nom du fichier (défaut: output.txt): ").strip()
        
        if not nom_fichier:
            nom_fichier = "output.txt"
        
        # Vérifier que le nom n'est pas vide après suppression des espaces
        if nom_fichier:
            return nom_fichier
        else:
            print("❌ Le nom du fichier ne peut pas être vide. Veuillez réessayer.")


def obtenir_texte_utilisateur():
    """Demande à l'utilisateur d'entrer du texte"""
    print("\nEntrez votre texte (tapez 'FIN' sur une nouvelle ligne pour terminer):")
    print("-" * 50)
    
    lignes = []
    while True:
        try:
            ligne = input()
            if ligne.upper() == "FIN":
                break
            lignes.append(ligne)
        except KeyboardInterrupt:
            print("\n\n⚠️  Opération annulée par l'utilisateur.")
            return None
        except EOFError:
            break
    
    return "\n".join(lignes)


def verifier_fichier_existant(nom_fichier):
    """Vérifie si le fichier existe et demande à l'utilisateur quoi faire"""
    if os.path.exists(nom_fichier):
        print(f"\n⚠️  Le fichier '{nom_fichier}' existe déjà.")
        while True:
            choix = input("Voulez-vous l'ajouter (a) ou le remplacer (r)? (a/r): ").strip().lower()
            if choix in ['a', 'r']:
                return choix
            else:
                print("❌ Veuillez entrer 'a' pour ajouter ou 'r' pour remplacer.")
    return 'r'  # Par défaut, remplacer si le fichier n'existe pas


def ecrire_fichier(nom_fichier, texte, mode='w'):
    """
    Écrit le texte dans le fichier
    
    Args:
        nom_fichier (str): Le nom du fichier
        texte (str): Le texte à écrire
        mode (str): 'w' pour remplacer, 'a' pour ajouter
    
    Returns:
        bool: True si succès, False sinon
    """
    try:
        # Vérifier les permissions d'écriture dans le répertoire
        repertoire = os.path.dirname(nom_fichier) or '.'
        if not os.access(repertoire, os.W_OK):
            print(f"❌ Erreur: Pas de permission d'écriture dans le répertoire '{repertoire}'")
            return False
        
        # Écrire dans le fichier
        with open(nom_fichier, mode, encoding='utf-8') as fichier:
            if mode == 'a' and os.path.getsize(nom_fichier) > 0:
                fichier.write('\n')  # Ajouter une ligne vide avant le nouveau texte
            fichier.write(texte)
        
        return True
    
    except PermissionError:
        print(f"❌ Erreur: Permission refusée. Impossible d'écrire dans '{nom_fichier}'")
        return False
    
    except IOError as e:
        if e.errno == 28:  # No space left on device
            print("❌ Erreur: Espace disque insuffisant pour écrire le fichier")
        else:
            print(f"❌ Erreur d'entrée/sortie: {e}")
        return False
    
    except UnicodeEncodeError:
        print("❌ Erreur: Impossible d'encoder le texte en UTF-8")
        return False
    
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False


def afficher_confirmation(nom_fichier, mode):
    """Affiche un message de confirmation"""
    try:
        taille = os.path.getsize(nom_fichier)
        taille_kb = taille / 1024
        
        if mode == 'w':
            action = "créé"
        else:
            action = "modifié"
        
        print("\n" + "="*50)
        print(f"✅ Succès! Le fichier '{nom_fichier}' a été {action}.")
        print(f"📊 Taille du fichier: {taille} octets ({taille_kb:.2f} KB)")
        print("="*50)
        
    except Exception as e:
        print(f"\n✅ Succès! Le fichier '{nom_fichier}' a été écrit.")
        print(f"⚠️  Impossible de vérifier la taille: {e}")


def afficher_contenu_fichier(nom_fichier):
    """Affiche le contenu du fichier écrit"""
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()
        
        print("\n" + "-"*50)
        print("CONTENU DU FICHIER:")
        print("-"*50)
        print(contenu)
        print("-"*50)
    
    except Exception as e:
        print(f"⚠️  Impossible d'afficher le contenu: {e}")


def mode_creation(nom_fichier=None):
    """Mode création d'un nouveau fichier"""
    if nom_fichier is None:
        nom_fichier = obtenir_nom_fichier()
    
    texte = obtenir_texte_utilisateur()
    
    if texte is None:
        return
    
    if not texte.strip():
        print("⚠️  Aucun texte à écrire. Opération annulée.")
        return
    
    if ecrire_fichier(nom_fichier, texte, mode='w'):
        afficher_confirmation(nom_fichier, 'w')
        
        choix = input("\nVoulez-vous afficher le contenu du fichier? (o/n): ").strip().lower()
        if choix == 'o':
            afficher_contenu_fichier(nom_fichier)
    else:
        print("❌ L'écriture du fichier a échoué.")


def mode_ajout(nom_fichier=None):
    """Mode ajout de texte à un fichier existant"""
    if nom_fichier is None:
        nom_fichier = obtenir_nom_fichier()
    
    if not os.path.exists(nom_fichier):
        print(f"⚠️  Le fichier '{nom_fichier}' n'existe pas.")
        choix = input("Voulez-vous le créer? (o/n): ").strip().lower()
        if choix == 'o':
            mode_creation(nom_fichier)
        return
    
    texte = obtenir_texte_utilisateur()
    
    if texte is None:
        return
    
    if not texte.strip():
        print("⚠️  Aucun texte à ajouter. Opération annulée.")
        return
    
    if ecrire_fichier(nom_fichier, texte, mode='a'):
        afficher_confirmation(nom_fichier, 'a')
        
        choix = input("\nVoulez-vous afficher le contenu du fichier? (o/n): ").strip().lower()
        if choix == 'o':
            afficher_contenu_fichier(nom_fichier)
    else:
        print("❌ L'ajout au fichier a échoué.")


def main():
    """Fonction principale"""
    print("\n🎯 Bienvenue dans le gestionnaire d'écriture de fichier!")
    
    while True:
        afficher_menu()
        
        try:
            choix = input("Choisissez une option (1/2/3): ").strip()
            
            if choix == '1':
                mode_creation()
            
            elif choix == '2':
                mode_ajout()
            
            elif choix == '3':
                print("\n👋 Au revoir!")
                sys.exit(0)
            
            else:
                print("❌ Option invalide. Veuillez choisir 1, 2 ou 3.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Programme interrompu par l'utilisateur. Au revoir!")
            sys.exit(0)
        
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")


if __name__ == "__main__":
    main()
