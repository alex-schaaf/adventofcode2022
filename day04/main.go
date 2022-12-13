package main

import (
	aoc "aoc/utils"
	"fmt"
	"strconv"
	"strings"
)

const filepath = "./input"

func parseLine(line string) [4]int {
	var intervals [4]int
	for i, section := range strings.Split(line, ",") {
		for j, intervalStr := range strings.Split(section, "-") {
			interval, err := strconv.Atoi(intervalStr)
			aoc.Handle(err)
			intervals[(i*2)+j] = interval
		}
	}
	return intervals
}

func main() {
	lines, err := aoc.ReadLines(filepath)
	aoc.Handle(err)

	var containments int
	var overlaps int
	for _, line := range lines {
		e := parseLine(line)

		if (e[0] >= e[2] && e[1] <= e[3]) || (e[2] >= e[0] && e[3] <= e[1]) {
			containments++
		}

		if e[1] >= e[2] && e[0] <= e[3] {
			overlaps++
		}
	}

	fmt.Println("Puzzle 1:", containments)
	fmt.Println("Puzzle 2:", overlaps)
}
