
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

        In this program, we consider a sequence of lines without an extra new line to be a stanza (kinda paragraph)

        The program returns the number of lines in each stanza as a list of numbers
        """

        previous_line = ""
        if len(input_text) > 0:
            stanzas = 1
        else:
            stanzas = 0

        nolines = 0
        stanzalengths = []
        for line in input_text:
            if line == "" and previous_line != "":
                stanzas += 1
                stanzalengths.append(nolines)
                nolines = 0
            elif line != "":
                nolines += 1
            previous_line = line

        if nolines != 0:
            stanzalengths.append(nolines)

        return ("No. of lines", stanzalengths)

    @staticmethod
    def evaluate(self, input_text, expected_value):
        result = self.analyze(input_text)
        if expected_value == result:
            return ("No. lines check", 1)
        else:
            return ("No. lines check", 0)


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


