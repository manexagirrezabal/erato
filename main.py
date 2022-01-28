# This is a sample Python script.

import argparse
from evaluators import generalEvaluator


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def evaluate_poem(file):
    poetry_evaluator = generalEvaluator()
    poetry_evaluator.load_model(directory="models/en")
    result = poetry_evaluator.analyze_file(file, output_format="pretty")  # we can also make it a table as output


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Please use this script to evaluate a poem')
    parser.add_argument('--filename', '-f', help="The file with the poem you want to analyze", default="input.txt")

    args = parser.parse_args()

    evaluate_poem(args.filename)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
