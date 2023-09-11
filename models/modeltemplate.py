
import sys

class evaluator(object):
    def __init__(self):
        pass

    def __str__(self):
        pass

    @staticmethod
    def analyze(input_text):
        """
        param input_text: This is the input text we want to analyze
        It will be a list of strings

        The program should return the output of the analysis as a tuple.
        The first element of the tuple is a string with the name of the analysis performed, and the second element should contain the 
result.
        """

        return ("", )

    @staticmethod
    def evaluate(self, input_text, expected_value):
        result = self.analyze(input_text)
        if expected_value == result:
            return ("check", 1)
        else:
            return ("check", 0)


if __name__ == '__main__':
    ev = evaluator()
    if len(sys.argv)>0:
        filename = sys.argv[1]
    else:
        filename = "../../../../data/poem1.txt"
    f=open(filename)
    lines=[line.strip() for line in f]
    f.close()
    counter = ev.analyze(lines)
    print (counter)


