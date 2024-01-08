
import sys
from nltk.tokenize import word_tokenize
import string

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

        The program returns the type/token ratio (lexical diversity)
        """

        text = " ".join(input_text)
        tokens = word_tokenize(text)
        filteredtokens = [tok for tok in tokens if tok not in string.punctuation]
        types = set(filteredtokens)

        return ("typetoken_ratio", len(types)/len(tokens))

    @staticmethod
    def evaluate(self, input_text, expected_value):
        result = self.analyze(input_text)
        if expected_value == result:
            return ("typetoken_ratiocheck", 1)
        else:
            return ("typetoken_ratiocheck", 0)


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
