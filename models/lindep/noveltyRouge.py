from rouge_metric import PyRouge

import pandas as pd
import numpy as np

from tqdm import tqdm

import sys

rouge = PyRouge(rouge_n=(1, 2, 3, 4),
                        rouge_l=True,
                        rouge_w=False,
                        rouge_s=False,
                        rouge_su=True,
                        skip_gap=4
                        )

def p1_p2_lbyl(lines1,lines2):
    #Compare poem1 with poem2 line by line
    results = []
    for indline, (line1,line2) in enumerate(zip(lines1,lines2)):
        scores = rouge.evaluate([line1], [[line2]])
        results.append(scores)

    accumulated_results=pd.DataFrame(results[0])
    for results_line in results[1:]:
        accumulated_results += pd.DataFrame(results_line)

    return accumulated_results/len(lines1)

def p1_p2_alllines (lines1,lines2):
    #Compare poem1 and poem2
    #line1 with line1,2,3,4...
    #line2 with line1,2,3,4...
    results = []
    for indline1, line1 in enumerate(lines1):
        for indline2,line2 in enumerate(lines2):
            scores = rouge.evaluate([line1], [[line2]])
            results.append(scores)

    accumulated_results=pd.DataFrame(results[0])
    for results_line in results[1:]:
        accumulated_results += pd.DataFrame(results_line)

    return accumulated_results/len(results)

def p1_p2_singlestr(lines1,lines2):
    #Compare poem1 and poem2 without considering the lines
    #We will concatenate all the lines together with " "
    poem1 = ' '.join(lines1)
    poem2 = ' '.join(lines2)
    scores = rouge.evaluate([poem1], [[poem2]])

    return pd.DataFrame(scores)


class evaluator(object):
    def __init__(self):
        pass

    def __str__(self):
        pass
    


    def _internal_analyze_func (analyses, texts, applied_fun):
        result_lbyl=[]
        poems = list(texts.keys())
        for poem1idx in tqdm(poems):
            for poem2idx in poems:
                if poem1idx != poem2idx:
                    result_lbyl.append(applied_fun(texts[poem1idx],texts[poem2idx]))
        accumulated_results_lbyl=pd.DataFrame(result_lbyl[0])
        for results_line in result_lbyl[1:]:
            accumulated_results_lbyl += pd.DataFrame(results_line)
        normalized_accumulated_results_lbyl =  accumulated_results_lbyl/((len(poems)-1) * (len(poems)))
        return normalized_accumulated_results_lbyl.loc['f'].values

    @staticmethod
    def analyze(analyses, texts):
        """
        param analyses: Independent text analyses of the texts that come in the second variable
        
        Example:
        
        {'data/eus_poems/bertsoa5.txt': {'stanzacount': 1, 'linecount': [10], 'syllablecount': [[7, 6, 7, 6, 7, 6, 7, 6, 7, 6]], 'intranovelty': {'rouge-1': 0.0, 'rouge-2': 0.0, 'rouge-3': 0.0, 'rouge-4': 0.0, 'rouge-l': 0.0, 'rouge-su4': 0.0}}, 'data/eus_poems/bertsoa4.txt': {'stanzacount': 1, 'linecount': [10], 'syllablecount': [[7, 7, 7, 6, 7, 6, 7, 6, 9, 6]], 'intranovelty': {'rouge-1': 0.01684303350970018, 'rouge-2': 0.0, 'rouge-3': 0.0, 'rouge-4': 0.0, 'rouge-l': 0.01684303350970018, 'rouge-su4': 0.002339181286549707}}, 
        
        param texts: This a dictionary with the texts we want to analyze
        The keys are the same as the analyses

        The program returns three cross-poem metrics
        """

        lbyl      = evaluator._internal_analyze_func(analyses, texts,p1_p2_lbyl)
        alllines  = evaluator._internal_analyze_func(analyses, texts,p1_p2_alllines)
        singlestr = evaluator._internal_analyze_func(analyses, texts,p1_p2_singlestr)

        

        
    
        return (("acrossnovelty (lbyl, alllines, singlestr)", (lbyl, alllines, singlestr)))

    @staticmethod
    def evaluate(self, input_text, expected_value):
        result = self.analyze(input_text)
        if expected_value == result:
            return ("intranoveltycheck", 1)
        else:
            return ("intranoveltycheck", 0)


if __name__ == '__main__':
    ev = evaluator()
    test_analyses = {'data/eus_poems/bertsoa5.txt': {'stanzacount': 1, 'linecount': [10], 'syllablecount': [[7, 6, 7, 6, 7, 6, 7, 6, 7, 6]], 'intranovelty': {'rouge-1': 0.0, 'rouge-2': 0.0, 'rouge-3': 0.0, 'rouge-4': 0.0, 'rouge-l': 0.0, 'rouge-su4': 0.0}}, 'data/eus_poems/bertsoa4.txt': {'stanzacount': 1, 'linecount': [10], 'syllablecount': [[7, 7, 7, 6, 7, 6, 7, 6, 9, 6]], 'intranovelty': {'rouge-1': 0.01684303350970018, 'rouge-2': 0.0, 'rouge-3': 0.0, 'rouge-4': 0.0, 'rouge-l': 0.01684303350970018, 'rouge-su4': 0.002339181286549707}}, 'data/eus_poems/bertsoa6.txt': {'stanzacount': 1, 'linecount': [10], 'syllablecount': [[7, 6, 7, 6, 7, 6, 6, 6, 9, 6]], 'intranovelty': {'rouge-1': 0.011111111111111112, 'rouge-2': 0.007407407407407407, 'rouge-3': 0.0, 'rouge-4': 0.0, 'rouge-l': 0.011111111111111112, 'rouge-su4': 0.007407407407407407}}, 'data/eus_poems/bertsoa3.txt': {'stanzacount': 1, 'linecount': [10], 'syllablecount': [[7, 6, 8, 6, 7, 6, 7, 6, 7, 6]], 'intranovelty': {'rouge-1': 0.016666666666666666, 'rouge-2': 0.0, 'rouge-3': 0.0, 'rouge-4': 0.0, 'rouge-l': 0.016666666666666666, 'rouge-su4': 0.013580246913580249}}, 'data/eus_poems/bertsoa2.txt': {'stanzacount': 1, 'linecount': [10], 'syllablecount': [[7, 6, 8, 6, 7, 6, 7, 6, 7, 6]], 'intranovelty': {'rouge-1': 0.022398589065255735, 'rouge-2': 0.0, 'rouge-3': 0.0, 'rouge-4': 0.0, 'rouge-l': 0.022398589065255735, 'rouge-su4': 0.002339181286549707}}, 'data/eus_poems/bertsoa1.txt': {'stanzacount': 1, 'linecount': [10], 'syllablecount': [[7, 6, 8, 6, 7, 6, 7, 6, 7, 6]], 'intranovelty': {'rouge-1': 0.00634920634920635, 'rouge-2': 0.0, 'rouge-3': 0.0, 'rouge-4': 0.0, 'rouge-l': 0.00634920634920635, 'rouge-su4': 0.0031746031746031746}}}
    test_texts = {'data/eus_poems/bertsoa5.txt': ['Ohean sartu zaigu', 'kolpera onduan', 'lapur gaizto ta trakets', 'hoietxen moduan', 'pixa egin ezazu', 'toki seguruan', 'kordea banatzeko', 'hemen inguruan', 'poltsa beroarekin', 'joko det buruan'], 'data/eus_poems/bertsoa4.txt': ['Nun ibili naizen ni', 'esan det lehenago', 'amonaren ondoan', 'ederki ez nago', 'izan ere edan det', 'horrenbeste ardo', 'gutxienez bazitun', 'hoitazazpi grado', 'bota egin behar det eta', 'oñala nun dago'], 'data/eus_poems/bertsoa6.txt': ['Poltsa beroarekin', 'hortxe jo nau danba', 'Ni ez naiz lotsatuko', 'egia esanda', 'amonan errezoa', 'holaxe izan da', 'Requiem est domine', 'virgo beneranda', 'gehio ez naiz etorriko', 'amona edanda'], 'data/eus_poems/bertsoa3.txt': ['Ez diot txartzat hartu', 'muxuka hastea', 'nahiz oraindik ez egon', 'holako gaztea', 'ez da gauza ederra', 'buru eskastea', 'hari tokatu behar', 'holako trastea', 'martiri bihurtu du', 'bere emaztea'], 'data/eus_poems/bertsoa2.txt': ['Gaur parrandan jo ta ke', 'hor dabil gizona', 'lehenen pasilloa jo', 'ta gero komona', 'uste nuen hau zala', 'nik nere moñoña', 'laztantzen hasi naiz ta', 'ez da horren ona', 'mozkorra nator eta', 'barkatu amona'], 'data/eus_poems/bertsoa1.txt': ['Batetikan korrozka', 'bestetik errena', 'ohia okupatu du', 'hori da txarrena', 'ez da pinta kabala', 'honek dakarrena', 'kantzontzilorik gabe', 'ohean barrena', 'pixkat gutxio edan', 'ezazu hurrena']}
    
    counter = ev.analyze(test_analyses,test_texts)
    print (counter)
