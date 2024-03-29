import expression_terminal
import plot_scores

import sys


def main(arg):
    # Your code goes here.
    # For example, print the argument:
    print(f"Running: {int(arg)} games")
    expression_terminal.run_expression_terminal(int(arg))
    print("Done! Plotting")
    plot_scores.plot_results()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_and_plot.py <argument>")
        sys.exit(1)

    argument = sys.argv[1]
    main(argument)

