# This is a sample Python script.

import argparse
from evaluators import generalSingleEvaluator,generalCollectionEvaluator


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def evaluate_poem(file, modeldir):
    poetry_evaluator = generalSingleEvaluator()
    poetry_evaluator.load_model()
    result = poetry_evaluator.analyze_file(file, output_format="pretty")  # we can also make it a table as output
    
def evaluate_poem_collection(directory):
    poem_collection_evaluator = generalCollectionEvaluator()
    poem_collection_evaluator.load_model()
    independent_analyses, global_analysis = poem_collection_evaluator.analyze_collection(directory)
    print ("Independent analysis")
    for bertso in independent_analyses.keys():
        print (bertso)
        print (independent_analyses[bertso])
    print ("Global analysis")
    print (global_analysis)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Please use this script to evaluate a poem or a collection of poems')
    parser.add_argument('--filename', '-f', help="The file with the poem you want to analyze", default="")
    parser.add_argument('--directory', '-d', help="The directory with the poem collection you want to analyze", default="")
    parser.add_argument('--list','-l',action="count",default=0)
    args = parser.parse_args()

    if args.list>0:
        poetry_evaluator = generalSingleEvaluator()
        poetry_evaluator.load_model()
        print ()
        for aspect in poetry_evaluator.evaluators.keys():
            print (aspect)
            print ("\t",poetry_evaluator.evaluators[aspect])
    elif args.filename:
        evaluate_poem(args.filename,args.model)
    elif args.directory:
        evaluate_poem_collection(args.directory)
        
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
