
from rouge_metric import PyRouge

import pandas as pd
import numpy as np

import sys

rouge = PyRouge(rouge_n=(1, 2, 3, 4),
                        rouge_l=True,
                        rouge_w=False,
                        rouge_s=False,
                        rouge_su=True,
                        skip_gap=4
                        )

class evaluator(object):
    def __init__(self):
        pass

    def __str__(self):
        pass

#    @staticmethod
    def analyze(input_text):
        """
        param input_text: This is the input text we want to analyze
        It will be a list of strings

        The program returns the number of stanzas
        """

        results = []
        for indline1, line1 in enumerate(input_text):
            for indline2, line2 in enumerate(input_text):
                if indline1 != indline2:
                    scores = rouge.evaluate([line1], [[line2]])
                    results.append(((indline1, indline2), scores))

        accumulated_results = pd.DataFrame(results[0][1])
        for results_line in results[1:]:
            accumulated_results += pd.DataFrame(results_line[1])

        normalized_accumulated_results = accumulated_results / len(results)
        return ("intranovelty", normalized_accumulated_results.loc["f"].to_dict())

    @staticmethod
    def evaluate(self, input_text, expected_value):
        result = self.analyze(input_text)
        if expected_value == result:
            return ("intranoveltycheck", 1)
        else:
            return ("intranoveltycheck", 0)


if __name__ == '__main__':
    ev = evaluator()
    if len(sys.argv)>1:
        filename = sys.argv[1]
    else:
        filename = "../../../data/poem1.txt"
    f=open(filename)
    lines=[line.strip() for line in f]
    f.close()
    counter = ev.analyze(lines)
    print (counter)
