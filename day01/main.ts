import fs from 'fs'

const contents = fs.readFileSync("./input", "utf-8")

const elves: number[][] = []
let elveCalories: number[] = []

contents.split("\n").forEach((line: string) => {
  if (!line) {
    elves.push(elveCalories)
    elveCalories = []
  } else {
    elveCalories.push(parseInt(line))
  }
})

const sums = elves.map(elf => elf.reduce((p, n) => p + n, 0))
const sortedSums = sums.sort((a, b) => b - a)

console.log(`Puzzle 1: ${sortedSums[0]}`)
console.log(`Puzzle 2: ${sortedSums.slice(0, 3).reduce((p, n) => p + n, 0)}`)