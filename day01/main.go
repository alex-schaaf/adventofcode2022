package main

import (
	aoc "aoc/utils"
	"fmt"
	"sort"
	"strconv"
)

const filepath = "./input"

func main() {
	lines, err := aoc.ReadLines(filepath)
	aoc.Handle(err)

	elves := [][]int{}

	calories := []int{}
	for _, line := range lines {
		if line == "" {
			elves = append(elves, calories)
			calories = []int{}
		} else {
			number, err := strconv.Atoi(line)
			aoc.Handle(err)
			calories = append(calories, number)
		}
	}

	var maxCalories int
	for _, elf := range elves {
		calories := aoc.Sum(elf)
		if calories > maxCalories {
			maxCalories = calories
		}
	}
	fmt.Println("Puzzle 1:", maxCalories)

	elveCalories := []int{}
	for _, elf := range elves {
		elveCalories = append(elveCalories, aoc.Sum(elf))
	}
	sort.Ints(elveCalories)

	fmt.Println("Puzzle 2:", aoc.Sum(elveCalories[len(elveCalories)-3:]))
}
