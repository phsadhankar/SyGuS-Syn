from cegis import CEGISSolver


def main():
    solver = CEGISSolver(
        max_size=9,
        timeout_seconds=30,
    )

    solution = solver.solve_max2()

    if solution is None:
        print("Solver failed to synthesize a valid expression.")
    else:
        print()
        print("Final answer:")
        print(solution)


if __name__ == "__main__":
    main()
