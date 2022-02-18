
import sys
#import nltk
#import re
from importlib import import_module
import importlib.util

module_name = "foma"
spec = importlib.util.spec_from_file_location("foma", "/Users/jbt694/project_poetryevaluation/erato/libs/foma.py")
module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module)

import foma

FSM = foma.FST()

def tokenize (s):
    return s.split(" ")

class silaba(object):

    def __init__(self):
        
        self.FSM = FSM.load("/Users/jbt694/project_poetryevaluation/erato/models/eu/silabaEus.fst")
        self.sildel = "."


    def silabatan(self, word):
        ress = self.FSM.apply_down(word)
#        return ress.next()
        return next(ress).decode()

    def silabakop(self, esaldi):
        esaldi=esaldi.lower()
        silkop = 0
        for word in tokenize(esaldi):
            res = self.silabatan(word)
            silkop+=len(res.split(self.sildel))

        return silkop





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
        s = silaba()
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
                noSyllsLine = s.silabakop(line)
                noSyllsStanza.append(noSyllsLine)

            previous_line = line

        if len(noSyllsStanza) != 0:
            noSyllsPoem.append(noSyllsStanza)

        return ("syllablecount", noSyllsPoem)

    @staticmethod
    def evaluate(self, input_text, expected_value):
        result = self.analyze(input_text)
        if expected_value == result:
            return ("syllablecheck", 1)
        else:
            return ("syllablecheck", 0)


if __name__ == '__main__':



    ev = evaluator()
    
    if len(sys.argv)>1:
        filename = sys.argv[1]
    else:
        filename = "../../../../data/poem1.txt"
    f=open(filename)
    lines=[line.strip() for line in f]
    f.close()
    counter = ev.analyze(lines)
    print (counter)

