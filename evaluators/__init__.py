
import pickle
import glob
from importlib import import_module
import importlib.util
import sys

class generalEvaluator(object):
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

    def load_model(self, directory="models/en"):

        #Load poetic feature model
        for filename in glob.glob(directory+"/poetic_features/*.py"):
            print ("Loading the file >"+filename)

            module_name = filename.split("/")[-1]
#            f=open(filename,"rb")
#            ev = pickle.load(f)
#            f.close()

            #ev = import_module(filename[-1], ".".join(filename[:-1]))
            spec = importlib.util.spec_from_file_location(module_name, filename)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            self.evaluators['poetic_features'].append(module.evaluator)


    def analyze_file(self, file:str, output_format="pretty"):
        lines = self.load_file(file)

        for evaluation_feature in self.evaluators.keys():
            for evaluator in self.evaluators[evaluation_feature]:
                result = evaluator.analyze(lines)
                print (result)




    @staticmethod
    def load_file(file: str) -> list:
        f = open(file, encoding="utf8")
        lines = [line.strip() for line in f]
        f.close()
        return lines



