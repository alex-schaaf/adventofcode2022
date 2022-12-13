package main

import (
	aoc "aoc/utils"
	"fmt"
	"sort"
)

const filepath = "./input"

type node struct {
	elevation int
	isTarget  bool
	neighbors []*node
	distance  int
}

func (n *node) addNeighbor(neighbor *node) {
	if neighbor.elevation <= n.elevation+1 {
		n.neighbors = append(n.neighbors, neighbor)
	}
}

func parseElevationRune(elevationRune rune) int {
	if elevationRune == 'S' {
		elevationRune = 'a'
	} else if elevationRune == 'E' {
		elevationRune = 'z'
	}
	return int(elevationRune) - 97
}

func breadthFirstSearch(startNode *node) {
	queue := []*node{}

	startNode.distance = 0
	queue = append(queue, startNode)

	for len(queue) > 0 {
		currentNode := queue[0]
		queue = queue[1:]

		for _, neighbor := range currentNode.neighbors {
			if neighbor.distance > 0 {
				continue
			}
			neighbor.distance = currentNode.distance + 1
			queue = append(queue, neighbor)
		}
	}
}

func main() {
	lines, err := aoc.ReadLines(filepath)
	aoc.Handle(err)

	nodes2D := [][]*node{}
	var startNode *node
	for _, line := range lines {
		nodeRow := []*node{}
		for _, elevationRune := range line {
			node := node{
				elevation: parseElevationRune(elevationRune),
				isTarget:  elevationRune == 'E',
				neighbors: []*node{},
				distance:  -1}

			if elevationRune == 'S' {
				startNode = &node
			}
			nodeRow = append(nodeRow, &node)
		}
		nodes2D = append(nodes2D, nodeRow)
	}

	for y, nodeRow := range nodes2D {
		for x, node := range nodeRow {
			if x > 0 {
				node.addNeighbor(nodes2D[y][x-1])
			}
			if x < len(nodeRow)-1 {
				node.addNeighbor(nodes2D[y][x+1])
			}
			if y > 0 {
				node.addNeighbor(nodes2D[y-1][x])
			}
			if y < len(nodes2D)-1 {
				node.addNeighbor(nodes2D[y+1][x])
			}
		}
	}

	nodes := aoc.Flatten(nodes2D)

	breadthFirstSearch(startNode)

	sort.Slice(nodes, func(i, j int) bool {
		return nodes[i].distance < nodes[j].distance
	})

	fmt.Println("Puzzle 1:", nodes[len(nodes)-1].distance)

	startingNodes := []*node{}
	for _, node := range nodes {
		if node.elevation == 0 {
			startingNodes = append(startingNodes, node)
		}
	}

	distances := []int{}
	for _, startNode := range startingNodes {

		for _, node := range nodes {
			node.distance = -1
		}

		breadthFirstSearch(startNode)
		for _, node := range nodes {
			if node.isTarget && node.distance > 0 {
				distances = append(distances, node.distance)
			}
		}
	}

	min := distances[0]
	for _, distance := range distances {
		if distance < min {
			min = distance
		}
	}

	fmt.Println("Puzzle 2:", min)
}
