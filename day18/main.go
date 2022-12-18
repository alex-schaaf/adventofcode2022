package main

import (
	aoc "aoc/utils"
	"fmt"
	"strconv"
	"strings"
)

const filename = "./input"

var DIRECTIONS = [6][3]int{
	{-1, 0, 0},
	{0, -1, 0},
	{0, 0, -1},
	{0, 0, 1},
	{0, 1, 0},
	{1, 0, 0},
}

func parse(line string) (int, int, int) {
	xyzStr := strings.Split(line, ",")
	x, _ := strconv.Atoi(xyzStr[0])
	y, _ := strconv.Atoi(xyzStr[1])
	z, _ := strconv.Atoi(xyzStr[2])
	return x, y, z
}

type Extent struct {
	x int
	X int
	y int
	Y int
	z int
	Z int
}

func getExtent(cubes map[[3]int]bool) Extent {
	var xs []int
	var ys []int
	var zs []int

	for cube := range cubes {
		xs = append(xs, cube[0])
		ys = append(ys, cube[1])
		zs = append(zs, cube[2])
	}

	return Extent{x: aoc.SliceMin(xs), X: aoc.SliceMax(xs) + 2, y: aoc.SliceMin(ys), Y: aoc.SliceMax(ys) + 2, z: aoc.SliceMin(zs), Z: aoc.SliceMax(zs) + 2}
}

func main() {

	lines, err := aoc.ReadLines(filename)
	aoc.Handle(err)

	cubes := map[[3]int]bool{}

	for _, line := range lines {
		x, y, z := parse(line)
		cube := [3]int{x + 1, y + 1, z + 1} // add buffer
		cubes[cube] = true
	}

	extent := getExtent(cubes)

	grid := [][][]uint8{}

	for x := extent.x; x <= extent.X; x++ {
		a := [][]uint8{}
		for y := extent.y; y <= extent.Y; y++ {
			b := []uint8{}
			for z := extent.z; z <= extent.Z; z++ {
				b = append(b, 0)
			}
			a = append(a, b)
		}
		grid = append(grid, a)
	}

	for c := range cubes {
		grid[c[0]][c[1]][c[2]] = 1
	}

	totalSurface := getSurfaceArea(cubes, grid, 0)
	fmt.Println("Puzzle 1:", totalSurface)

	grid = floodFill(grid, [3]int{0, 0, 0})

	outerSurface := getSurfaceArea(cubes, grid, 2)
	fmt.Println("Puzzle 2:", outerSurface)
}

func floodFill(grid [][][]uint8, start [3]int) [][][]uint8 {
	queue := [][3]int{}
	queue = append(queue, start)

	for len(queue) > 0 {
		point := queue[0]
		queue = queue[1:]

		value := grid[point[0]][point[1]][point[2]]
		if value != 0 {
			continue
		}

		grid[point[0]][point[1]][point[2]] = 2

		for _, d := range DIRECTIONS {
			x := point[0] + d[0]
			y := point[1] + d[1]
			z := point[2] + d[2]
			p := [3]int{x, y, z}

			if inBounds(grid, p) {
				queue = append(queue, p)
			}

		}
	}

	return grid
}

func inBounds(grid [][][]uint8, p [3]int) bool {
	x := p[0]
	y := p[1]
	z := p[2]
	if 0 <= x && x < len(grid) && 0 <= y && y < len(grid[0]) && 0 <= z && z < len(grid[0][0]) {
		return true
	}
	return false
}

func getSurfaceArea(cubes map[[3]int]bool, grid [][][]uint8, value uint8) int {
	var surface int

	for point := range cubes {
		for _, d := range DIRECTIONS {
			x := point[0] + d[0]
			y := point[1] + d[1]
			z := point[2] + d[2]
			p := [3]int{x, y, z}

			if inBounds(grid, p) && grid[x][y][z] == value {
				surface++
			}
		}
	}

	return surface
}
