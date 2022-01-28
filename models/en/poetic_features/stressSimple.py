
import sys
import nltk
import re

num_regexp = re.compile("\d")
vow_regexp = re.compile("[aeiou]")
nonalphanumeric_regex = re.compile("[^a-zA-Z\ \']")
cmudict = nltk.corpus.cmudict.dict()


def getStresses(line):
    line = re.sub(nonalphanumeric_regex, "", line)
    linev = line.lower().split(" ")
    totalnosylls = []
    for word in linev:

        phonemes = "".join(cmudict.get(word, "-")[0])
        if phonemes == "-":
            stresses = ["-"]
        else:
            stress_numbers = re.findall(num_regexp,phonemes)
            stresses = ["-" if el=='0' else "+" for el in stress_numbers]
#        print (word,nosylls)
        totalnosylls += stresses
    return "".join(totalnosylls)


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
        noSyllsStanza = []
        noSyllsPoem = []
        for line in input_text:
            if line == "" and previous_line != "":
                noSyllsPoem.append(noSyllsStanza)
                noSyllsStanza = []
                nolines = 0
            elif line != "":
                noSyllsLine = getStresses(line)
                noSyllsStanza.append(noSyllsLine)

            previous_line = line

        if len(noSyllsStanza) != 0:
            noSyllsPoem.append(noSyllsStanza)

        return ("Stresses", noSyllsPoem)

    @staticmethod
    def evaluate(self, input_text, expected_value):
        result = self.analyze(input_text)
        if expected_value == result:
            return ("Stress check", 1)
        else:
            return ("Stress check", 0)


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

