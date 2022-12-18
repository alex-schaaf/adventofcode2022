# advent of code 2022

🎄

## Solutions

⚠️ Spoiler alert ⚠️

1. [Go](https://github.com/alex-schaaf/adventofcode2022/blob/main/day01/main.go) | [Python](https://github.com/alex-schaaf/adventofcode2022/blob/main/day01/main.py) | [TypeScript](https://github.com/alex-schaaf/adventofcode2022/blob/main/day01/main.ts)
2. [Go](https://github.com/alex-schaaf/adventofcode2022/blob/main/day02/main.go)
3. [Go](https://github.com/alex-schaaf/adventofcode2022/blob/main/day03/main.go) | [Python](https://github.com/alex-schaaf/adventofcode2022/blob/main/day03/main.py)
4. [Go](https://github.com/alex-schaaf/adventofcode2022/blob/main/day04/main.go) | [Python](https://github.com/alex-schaaf/adventofcode2022/blob/main/day04/main.py)
5. [Python](https://github.com/alex-schaaf/adventofcode2022/blob/main/day05/main.py)
6. [Python](https://github.com/alex-schaaf/adventofcode2022/blob/main/day06/main.py)
7. [Python](https://github.com/alex-schaaf/adventofcode2022/blob/main/day07/main.py)
8. [Python](https://github.com/alex-schaaf/adventofcode2022/blob/main/day08/main.py)
9. [Python](https://github.com/alex-schaaf/adventofcode2022/blob/main/day09/main.py)
10. [Python](https://github.com/alex-schaaf/adventofcode2022/blob/main/day10/main.py)
11. [Python](https://github.com/alex-schaaf/adventofcode2022/blob/main/day11/main.py)
12. [Go](https://github.com/alex-schaaf/adventofcode2022/blob/main/day12/main.go) | [Python](https://github.com/alex-schaaf/adventofcode2022/blob/main/day12/main.py)
13. [Python](https://github.com/alex-schaaf/adventofcode2022/blob/main/day13/main.py)
14. [Python](https://github.com/alex-schaaf/adventofcode2022/blob/main/day14/main.py)
    - Started out by using a 2-D array as a world map. This was a bad idea as it
      required either creating a very large array due to the action being centered
      around `x=500` or dealing with confusing offsets through the code. After
      scrapping that approach I used a `defaultdict` as a sparse matrix mapping
      points to tiles, only keeping track of the non-empty tiles. 15. 16.
15. [Python (Part 1)](https://github.com/alex-schaaf/adventofcode2022/blob/main/day17/main.py)
16. [Python](https://github.com/alex-schaaf/adventofcode2022/blob/main/day18/main.py)
    - Solved the first part without using a 3D array but rather a set of rock
      coordinate tuples, looping over them and checking if their direct
      neighbors are also in the set of rock coordinates. But this then led me to
      to some weird attempts to flood fill the surroundings of each rock to
      check if it leaks to the outside. After a while it hit me to just flood
      fill a 3D array from the outside of the rock structure once 😅

## Performance

| Command      |   Mean [ms] | Min [ms] | Max [ms] | Relative |
| :----------- | ----------: | -------: | -------: | -------: |
| `./day01`    |   4.4 ± 0.1 |      4.2 |      5.1 |     1.00 |
| `./day02`    |   5.2 ± 0.1 |      5.0 |      5.7 |     1.00 |
| `./day03`    |  10.2 ± 0.2 |     10.0 |     10.9 |     1.00 |
| `./day04`    |   4.6 ± 0.1 |      4.4 |      5.4 |     1.00 |
| `./day12`    |  85.5 ± 1.8 |     82.2 |     90.2 |     1.00 |
| `./day13.py` | 416.4 ± 1.7 |    414.3 |    420.2 |     1.00 |

Runtime measured using [`hyperfine`](https://github.com/sharkdp/hyperfine) on
MacBook Pro 16-inch 2019 with 2,6 GHz 6-Core Intel Core i7 and 16 GB 2667 MHz
DDR4 running macOS Ventura.

```
hyperfine ./filename --export-markdown perf.md -N --warmup=10
```

## Previous years

- [2021](https://github.com/alex-schaaf/adventofcode2021)
- [2020](https://github.com/alex-schaaf/adventofcode2020)
- [2019](https://github.com/alex-schaaf/adventofcode2019)
