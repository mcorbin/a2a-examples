package main

import (
	"crypto/rand"
	"fmt"
)

// generateUUIDv4 generates a random UUID v4
func generateUUIDv4() string {
	b := make([]byte, 16)
	_, err := rand.Read(b)
	if err != nil {
		panic(err)
	}

	// Set version to 4
	b[6] = (b[6] & 0x0f) | 0x40

	// Set variant to RFC 4122
	b[8] = (b[8] & 0x3f) | 0x80

	return fmt.Sprintf("%x-%x-%x-%x-%x",
		b[0:4], b[4:6], b[6:8], b[8:10], b[10:16])
}

func main() {
	// Generate a UUID v4
	uuid := generateUUIDv4()

	// Display the generated UUID
	fmt.Println("Generated UUID v4:", uuid)
}
