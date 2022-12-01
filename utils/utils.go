package utils

import (
	"bufio"
	"log"
	"os"
)

// Handle a given error.
func Handle(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

func ReadLines(filepath string) ([]string, error) {
	file, err := os.Open(filepath)
	Handle(err)
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines, scanner.Err()
}

func Sum(arr []int) int {
	var sum int
	for _, elem := range arr {
		sum += elem
	}
	return sum
}
