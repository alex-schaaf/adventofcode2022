package main

import (
	aoc "aoc/utils"
	"fmt"
	"strings"
)



func main() {
	shapes := map[string]string{
		"A": "Rock",
		"B": "Paper",
		"C": "Scissors",
		"X": "Rock",
		"Y": "Paper",
		"Z": "Scissors",
	}

	scores := map[string]int{
		"Rock": 1,
		"Paper": 2,
		"Scissors": 3,
	}

	const lost = 0
	const draw = 3
	const won = 6

	lines, err := aoc.ReadLines("./input")
	aoc.Handle(err)

	var score int
	for _, line := range lines {
		split := strings.Split(line, " ")
		opponent := split[0]
		self := split[1]

		opponentShape := shapes[opponent]
		selfShape := shapes[self]

		opponentScore := scores[opponentShape]
		selfScore := scores[selfShape]


		score += selfScore
		if selfScore == opponentScore {
			score += draw
		} else if (
			(selfShape == "Rock" && opponentShape == "Scissors") || (selfShape == "Scissors" && opponentShape == "Paper") || (selfShape == "Paper" && opponentShape == "Rock")) {
				score += won
		} else {
			score += lost
		}

	}
	fmt.Println("Puzzle 1:", score)


	score = 0
	for _, line := range lines {
		split := strings.Split(line, " ")
		opponent := split[0]
		self := split[1]

		opponentShape := shapes[opponent]

		var selfShape string
		if self == "X" { // lose
			switch opponentShape {
			case "Rock":
				selfShape = "Scissors"
			case "Paper":
				selfShape = "Rock"
			case "Scissors":
				selfShape = "Paper"
			}
		} else if self == "Y" { // draw
			selfShape = opponentShape
		} else { // win
			switch opponentShape {
			case "Rock":
				selfShape = "Paper"
			case "Paper":
				selfShape = "Scissors"
			case "Scissors":
				selfShape = "Rock"
			}
		}

		opponentScore := scores[opponentShape]
		selfScore := scores[selfShape]


		score += selfScore
		if selfScore == opponentScore {
			score += draw
		} else if (
			(selfShape == "Rock" && opponentShape == "Scissors") || (selfShape == "Scissors" && opponentShape == "Paper") || (selfShape == "Paper" && opponentShape == "Rock")) {
				score += won
		} else {
			score += lost
		}

	}
	fmt.Println("Puzzle 2:", score)
}

