#!/usr/bin/env python3
"""
Script pour lire et afficher le contenu d'un fichier.

Usage:
    python3 read_file.py <chemin_du_fichier>

Exemple:
    python3 read_file.py /chemin/vers/mon/fichier.txt
"""

import sys
import os


def main():
    """
    Fonction principale qui gère la lecture et l'affichage du fichier.
    """
    
    # Vérifier que le nombre d'arguments est correct
    if len(sys.argv) != 2:
        print("Erreur: nombre d'arguments incorrect")
        print("Usage: python3 read_file.py <chemin_du_fichier>")
        sys.exit(1)
    
    # Récupérer le chemin du fichier depuis les arguments
    file_path = sys.argv[1]
    
    # Vérifier que le fichier existe
    if not os.path.exists(file_path):
        print(f"Erreur: le fichier '{file_path}' n'existe pas")
        sys.exit(1)
    
    # Vérifier que c'est bien un fichier (et pas un répertoire)
    if not os.path.isfile(file_path):
        print(f"Erreur: '{file_path}' n'est pas un fichier")
        sys.exit(1)
    
    # Vérifier les permissions de lecture
    if not os.access(file_path, os.R_OK):
        print(f"Erreur: permissions insuffisantes pour lire '{file_path}'")
        sys.exit(1)
    
    # Essayer de lire et afficher le contenu du fichier
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contenu = file.read()
            
            # Afficher le contenu
            print(f"=== Contenu du fichier: {file_path} ===\n")
            print(contenu)
            print(f"\n=== Fin du fichier ===")
            
    except UnicodeDecodeError:
        print(f"Erreur: impossible de décoder le fichier '{file_path}'")
        print("Le fichier ne semble pas être un fichier texte UTF-8")
        sys.exit(1)
    except IOError as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
