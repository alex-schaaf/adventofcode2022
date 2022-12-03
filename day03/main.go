package main

import (
	aoc "aoc/utils"
	"errors"
	"fmt"
)

const PRIORITIES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

func findDuplicate(c1, c2 string) (rune, error) {
	for _, item1 := range c1 {
		for _, item2 := range c2 {
			if (item1 == item2) {
				return item1, nil
			}
		}
	}
	return 0, errors.New("No duplicate item found")
}

func getPriority(item rune) (int, error) {
	for i, ch := range PRIORITIES {
		if (ch == item) {
			return i + 1, nil
		}
	}
	return 0, errors.New("Unable to prioritize item")
}

func main() {
	rucksacks, err := aoc.ReadLines("./input")
	aoc.Handle(err)

	var prioritiesSum int
	for _, rucksack := range rucksacks {
		middle := len(rucksack) / 2
		c1 := rucksack[:middle]
		c2 := rucksack[middle:]

		duplicate, _ := findDuplicate(c1, c2)
		
		priority, _ := getPriority(duplicate)
		prioritiesSum += priority
	}
	fmt.Println("Puzzle 1:", prioritiesSum)

	prioritiesSum = 0
	for i := 0; i < len(rucksacks); i += 3 {
		rucksackGroup := rucksacks[i:i+3]

		var badge rune
		for _, item1 := range rucksackGroup[0] {
			for _, item2 := range rucksackGroup[1] {
				for _, item3 := range rucksackGroup[2] {
					if (item1 == item2 && item1 == item3) {
						badge = item1
					}
				}
				
			}
		}
		priority, _ := getPriority(badge)
		prioritiesSum += priority
	}
	fmt.Println("Puzzle 2:", prioritiesSum)
}

