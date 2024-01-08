
#https://github.com/versotym/rhymeTagger

#from generalevaluator import generalevaluator
#from models.lindep.generalevaluator import generalevaluator

import sys
import glob

import re

from rhymetagger import RhymeTagger

rt = RhymeTagger()
rt.load_model(model='en',verbose=False)


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

        The program returns a dictionary with the analysis of the rhymes of a poem. It returns two values. One is the number of different rhymes (vocabulary) and the other is the ratio between the number of rhyming lines with the total numbner of lines (empty lines not counted).

        We call an ending a rhyme if it is repeated across the work. If a line does not rhyme with any other line it will not be counted as a rhyming line.
        """
        
        clean_text = [re.sub("[^a-zA-Z\ \']", "", text) for text in input_text]

        rhymes = rt.tag(clean_text, output_format=3) 

        norhymes = len([rhyme for rhyme in rhymes if rhyme is not None])
        nolines = len([line for line in input_text if line.strip()!=""])
        
        rhymevocab = set(rhymes)
        
        if None in rhymevocab:
            rhymevocab.remove(None)

#        print ("No. different rhymes", len(set(rhymes)))
#        print ("Rhyme ratio per no. of lines", norhymes/nolines)
#        print (len(rhymevocab),norhymes/nolines)
#        print ()

        return ("rhyme", {"no_rhymes":len(rhymevocab),"rhymerichness":norhymes/nolines})
    
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
        filename = "../../../../data/poem1.txt"
    f=open(filename)
    lines=[line.strip() for line in f]
    f.close()
    counter = ev.analyze(lines)
    print (counter)
