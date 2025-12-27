package main

import (
	"fmt"
	"os"
)

func main() {
	// Contenu à écrire dans le fichier
	content := `Bonjour, ceci est un fichier texte créé par un script Go.
Ce fichier contient du contenu basique.
Il a été généré automatiquement.
`

	// Créer et écrire dans le fichier "output.txt"
	// os.WriteFile crée le fichier s'il n'existe pas, ou le remplace s'il existe
	// 0644 sont les permissions du fichier (lecture/écriture pour le propriétaire)
	err := os.WriteFile("output.txt", []byte(content), 0644)

	// Vérifier s'il y a eu une erreur
	if err != nil {
		fmt.Println("Erreur lors de la création du fichier:", err)
		return
	}

	// Afficher un message de succès
	fmt.Println("Fichier 'output.txt' créé avec succès!")
}
