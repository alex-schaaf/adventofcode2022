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

func SliceSum(arr []int) int {
	var sum int
	for _, elem := range arr {
		sum += elem
	}
	return sum
}

func SliceAny(arr []bool) bool {
	for _, elem := range arr {
		if elem {
			return true
		}
	}
	return false
}

func SliceAll(arr []bool) bool {
	for _, elem := range arr {
		if !elem {
			return false
		}
	}
	return true
}

func SliceMax(arr []int) int {
	max := arr[0]
	for _, elem := range arr {
		if elem > max {
			max = elem
		}
	}
	return max
}

func SliceMin(arr []int) int {
	min := arr[0]
	for _, elem := range arr {
		if elem < min {
			min = elem
		}
	}
	return min
}

func SliceNth[T any](arr []T, n int) []T {
	var res []T
	for i, elem := range arr {
		if i%n == 0 {
			res = append(res, elem)
		}
	}
	return res
}

// Flatten a 2-dimensional slice.
func Flatten[T any](lists [][]T) []T {
	var res []T
	for _, list := range lists {
		res = append(res, list...)
	}
	return res
}

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}
