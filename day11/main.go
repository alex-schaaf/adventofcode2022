package main

import (
	aoc "aoc/utils"
	"fmt"
	"math"
	"regexp"
	"sort"
	"strconv"
)

const filepath = "./input"

func puzzle(monkeys []*Monkey, rounds, mod int) {
	for round := 0; round < rounds; round++ {
		for _, monkey := range monkeys {
			monkey.HandleItems(monkeys, mod)
		}
	}

	sort.Slice(monkeys, func(i, j int) bool {
		return monkeys[i].nInspections > monkeys[j].nInspections
	})

	fmt.Println("Puzzle:", monkeys[0].nInspections*monkeys[1].nInspections)
}

func main() {
	lines, err := aoc.ReadLines(filepath)
	aoc.Handle(err)
	monkeys := parse(lines)
	puzzle(monkeys, 20, 0)

	monkeys = parse(lines)
	mod := 1
	for _, monkey := range monkeys {
		mod *= monkey.divisibleBy
	}
	puzzle(monkeys, 10_000, mod)
}

type Operation func(int) int

type Monkey struct {
	items        []int
	operation    Operation
	divisibleBy  int
	ifTrue       int
	ifFalse      int
	nInspections int
}

func (m *Monkey) Test(worryLevel int) int {
	if worryLevel%m.divisibleBy == 0 {
		return m.ifTrue
	} else {
		return m.ifFalse
	}
}

func (m *Monkey) HandleItems(monkeys []*Monkey, mod int) {
	for len(m.items) > 0 {
		item := m.items[0]
		m.items = m.items[1:]
		m.nInspections += 1

		worryLevel := m.operation(item)
		if mod > 0 {
			worryLevel %= mod
		} else {
			worryLevel = int(math.Floor(float64(worryLevel) / 3))
		}
		target := m.Test(worryLevel)

		monkeys[target].items = append(monkeys[target].items, worryLevel)
	}
}

func parse(lines []string) []*Monkey {
	var monkeys []*Monkey
	rNum, _ := regexp.Compile("\\d+")
	rOperator, _ := regexp.Compile("[*+-/]")

	for i := 0; i < len(lines); i += 7 {
		startingItemsStr := rNum.FindAllString(lines[i+1], -1)
		var startingItems []int
		for _, itemStr := range startingItemsStr {
			item, _ := strconv.Atoi(itemStr)
			startingItems = append(startingItems, item)
		}

		factor, err := strconv.Atoi(rNum.FindString(lines[i+2]))
		operator := rOperator.FindString(lines[i+2])

		var operation Operation
		if err != nil {
			operation = func(old int) int {
				return old * old
			}
		} else {
			switch operator {
			case "+":
				operation = func(old int) int {
					return old + factor
				}
			case "-":
				operation = func(old int) int {
					return old - factor
				}
			case "*":
				operation = func(old int) int {
					return old * factor
				}
			case "/":
				operation = func(old int) int {
					return old / factor
				}
			}
		}

		divisibleBy, _ := strconv.Atoi(rNum.FindString(lines[i+3]))
		ifTrue, _ := strconv.Atoi(rNum.FindString(lines[i+4]))
		ifFalse, _ := strconv.Atoi(rNum.FindString(lines[i+5]))

		monkey := Monkey{items: startingItems, divisibleBy: divisibleBy, ifTrue: ifTrue, ifFalse: ifFalse, operation: operation}
		monkeys = append(monkeys, &monkey)
	}
	return monkeys
}
