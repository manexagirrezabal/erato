
import sys
import nltk
import re

num_regexp = re.compile("\d")
vow_regexp = re.compile("[aeiou]")
nonalphanumeric_regex = re.compile("[^a-zA-Z\ \']")
cmudict = nltk.corpus.cmudict.dict()


def countSyllables(line):
    line = re.sub(nonalphanumeric_regex, "", line)
    linev = line.lower().split(" ")
    totalnosylls = 0
    for word in linev:

        phonemes = "".join(cmudict.get(word, "-")[0]) #TODO: Use the minimum and maximum number of syllables
        if phonemes == "-":
            nosylls = len(re.findall(vow_regexp,word))
        else:
            nosylls = len(re.findall(num_regexp,phonemes))
#        print (word,nosylls)
        totalnosylls += nosylls
    return totalnosylls


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
                noSyllsLine = countSyllables(line)
                noSyllsStanza.append(noSyllsLine)

            previous_line = line

        if len(noSyllsStanza) != 0:
            noSyllsPoem.append(noSyllsStanza)

        return ("No. of syllables per line", noSyllsPoem)

    @staticmethod
    def evaluate(self, input_text, expected_value):
        result = self.analyze(input_text)
        if expected_value == result:
            return ("No. syllables check", 1)
        else:
            return ("No. syllables check", 0)


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

