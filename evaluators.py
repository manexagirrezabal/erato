
import pickle
import glob
from importlib import import_module
import importlib.util
import sys

from tqdm import tqdm

import pandas as pd

from models import singlemodels,collectionmodels

def load_file(file: str) -> list:
    f = open(file, encoding="utf8")
    lines = [line.strip() for line in f]
    f.close()
    return lines

'''
This is a class defined for general evaluators that can be used to analyze a poem independently.
For example one of the evaluators could be the system that counts the number of syllables.
This syllable counting does not depend on other poems/files.
'''
class generalSingleEvaluator(object):
    def __init__(self):
        self.evaluators = {}
        self.initialize_evaluators()

    def __str__(self):
        pass

    def initialize_evaluators(self):

#       Load poetic feature evaluators
        self.evaluators['poetic_features'] = []

#       Load lexical/semantic feature evaluators
        self.evaluators['lexsem_features'] = []

#       Load novelty evaluators
        self.evaluators['novelty_features'] = []

#       Load fluency evaluators
        self.evaluators['fluency_features'] = []
    
    def _load_model(self,models=singlemodels):
        for aspect in models:
            for filename in models[aspect]:
                print ("Loading the file >"+filename)

                module_name = filename.split("/")[-1]

                spec = importlib.util.spec_from_file_location(module_name, filename)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                self.evaluators[aspect].append(module.evaluator)

    def load_model(self, models=singlemodels):
        print ("Load single poem analyzers")
        self._load_model(models)
        


    def analyze_file(self, file:str, output_format="pretty", verbose=None):
        lines = load_file(file)
        
        whole_result = []
        for evaluation_feature in self.evaluators.keys():
            for evaluator in self.evaluators[evaluation_feature]:
                result = evaluator.analyze(lines)
                if verbose:
                    print (result)
                whole_result.append(result)
        whole_result_dict = {el[0]:el[1] for el in whole_result}
        return whole_result_dict,lines

'''
This is the class for the evaluators that need more than a single file to evaluate.
In this class we do not evaluate a single poem, but we evaluate a collection of poems,
 meaning that we evaluate a system/author.
There are other aspects, though, that require more files. For example:
 Evaluating whether two-three generated poems are too similar to each other
 Evaluating whether the topic that the poems cover is good enough (information retrieval approach)
'''
class generalCollectionEvaluator(generalSingleEvaluator):
    def __init__(self):
        super().__init__()
        
    def __str__(self):
        pass

    def load_model(self):
        print ("Load general models:")
        super()._load_model(models=collectionmodels)

    def analyze_collection(self,directory,verbose=None):
        poetry_evaluator = generalSingleEvaluator()
        poetry_evaluator.load_model()
        independent_analyses={}
        independent_texts  ={}
        for filename in tqdm(glob.glob(directory+"/*.txt")):
            independent_analyses[filename],independent_texts[filename] = poetry_evaluator.analyze_file(filename, output_format="pretty")
        pd.DataFrame(independent_analyses).to_csv("independent_analyses.csv")
        #print (independent_analyses)
        
        
        #Now the general evaluator comes into play
        final_result = []
        for evaluation_feature in self.evaluators.keys():
            for evaluator in self.evaluators[evaluation_feature]:
                local_result = evaluator.analyze(independent_analyses,independent_texts)
                if verbose:
                    print (local_result)
                final_result.append(local_result)
        final_result_dict = {el[0]:el[1] for el in final_result}
        #print (final_result_dict)
        
        return independent_analyses, final_result_dict
