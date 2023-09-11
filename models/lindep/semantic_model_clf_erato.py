
#conda activate poetryevaluation

#import pandas as pd
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import numpy as np

from matplotlib import pyplot as plt
        
from sklearn.metrics import classification_report,f1_score

from tqdm import tqdm
import sys

def cosine_similarity(v1, v2):
    return np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))

model = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v1')
get_representation = model.encode


class evaluator(object):
    def __init__(self):
        pass
        
    def __str__(self):
        pass
    
    @staticmethod
    def load_topics(directory):
        #This function expects a directory with the folllowing structure:
        #gaiN.txt or topicN.txt
        # This file contains the topic in a string
        #aldiN (directory) or poemsN, where some *.txt files are
        # These *.txt are poems that are related to the topics defined in gaiN.txt
        
        
        texts=[]
        topics=[]
        for bertsoaldi in glob.glob(directory+"/poems*"):
            #If topic is given:
            print (bertsoaldi)
            bertsoaldiv = bertsoaldi.split("/")
            basedir = "/".join(bertsoaldiv[:-1])+"/"
            topicno = bertsoaldiv[-1].split("s")[-1]
            print (basedir, topicno)
            
            f=open(basedir+"topic"+topicno+".txt")
            topic = f.readline().strip()
            f.close()
            #If not,
            #topic=bertsoaldi
            for bertso in glob.glob(bertsoaldi+"/*.txt"):
                f=open(bertso)
                lines = " ".join([line.strip() for line in f])
                f.close()

                texts.append(lines)
                topics.append(topic)
    
        #If the topic is a directory name, convert them to a readable number
        topics_v = sorted(set(topics))
        notopics = len(topics_v)
        topic_idx = {topic:idx for idx,topic in enumerate(topics_v)}
        topicids = [topic_idx[topic] for topic in topics]
        print ("topic_idx",topic_idx)

        return texts,topics,topicids,topic_idx

    @staticmethod
    def analyze (analyses,texts):
        """
        param analyses: Independent text analyses of the texts that come in the second variable
        
        Example:
        
        {'data/eus_poems/bertsoa5.txt': {'stanzacount': 1, 'linecount': [10], 'syllablecount': [[7, 6, 7, 6, 7, 6, 7, 6, 7, 6]], 'intranovelty': {'rouge-1': 0.0, 'rouge-2': 0.0, 'rouge-3': 0.0, 'rouge-4': 0.0, 'rouge-l': 0.0, 'rouge-su4': 0.0}}, 'data/eus_poems/bertsoa4.txt': {'stanzacount': 1, 'linecount': [10], 'syllablecount': [[7, 7, 7, 6, 7, 6, 7, 6, 9, 6]], 'intranovelty': {'rouge-1': 0.01684303350970018, 'rouge-2': 0.0, 'rouge-3': 0.0, 'rouge-4': 0.0, 'rouge-l': 0.01684303350970018, 'rouge-su4': 0.002339181286549707}}, 
        
        param texts: This a dictionary with the texts we want to analyze
        The keys are the same as the analyses

        The program returns the semantic evaluation based on a classification model
        """
        
        docs = []
        topics = []
        
        poems = list(texts.keys())
        for poemfileaddress in tqdm(poems):
            filename = poemfileaddress.split("/")[-1]
            fileaddress = "/".join(poemfileaddress.split("/")[:-1])
            
            poemno,topicfile = filename.split("-")
            
            f=open(fileaddress +"/"+ topicfile)
            topic = f.readline().strip()
            f.close()
            
            docs.append(texts[poemfileaddress])
            topics.append(topic)
            
        topics_v = list(sorted(set(topics)))
        topic_idx = {topic:idx for idx,topic in enumerate(topics_v)}
        topicids = [topic_idx[topic] for topic in topics]
        
        

        return evaluator._internal_analyze_func(docs, topics, topicids, topic_idx)

    @staticmethod
    def _internal_analyze_func(texts, topics,topicids,topicidx,verbose=False):
        """
        param texts: This a list with the texts we want to analyze
        The keys are the same as the analyses

        The program returns three cross-poem metrics
        """

        idx2topic = {topicidx[topic]:topic for topic in topicidx.keys()}
        print ("idx2topic",idx2topic)
        topicv=list(sorted(idx2topic.keys()))
        distances = np.zeros((len(texts),len(topicv)))
        for indtext,text in tqdm(enumerate(texts)):
            textrep = get_representation(" ".join(text))
            for indtopic,topic in enumerate(topicv):
                
                topicrep = get_representation(idx2topic[topic])

                #Instead of encoding the whole poem as such,
                #calculate similarities between the topic and each poem line (verse)
                #and calculate the average cosine distance
                #Maybe min/max cosine distance?
                print (idx2topic[topic])
                print (text)
                print ()
                
                distances[indtext][indtopic] = cosine_similarity(textrep,topicrep)
                if verbose:
                    print (idx2topic[topic])
                    print (text)
                    print (distances[indtext][indtopic])
                    print (indtext,indtopic,distances.shape)
                    print ()
                    
        predicted_topicids = np.array(np.argmax(distances,axis=1),dtype=int)
        predicted_topics = [idx2topic[el] for el in predicted_topicids]
        
        
        print ("Actual topics",topics)
        print ("Actual topic ids",topicids)
        print ()
        print ("Recall analysis")
        print ("Topic idx (dictionary)",topicidx) #Topic dictionary
        print ("Predicted topic for each poem",predicted_topics)
        print (classification_report(topics,predicted_topics))
        print (distances)

        true_topn = {topic:np.argwhere(topicids==topic).reshape(-1) for topic in topicv}
        
#        plt.imshow(distances)
#        plt.colorbar()
#        plt.show()
        result=f1_score(topics,predicted_topics, average="macro")
        
    
        return (("f1score semantics", (result)))

    @staticmethod
    def evaluate(self, input_text, expected_value):
        result = self.analyze(input_text)
        if expected_value == result:
            return ("intranoveltycheck", 1)
        else:
            return ("intranoveltycheck", 0)


if __name__ == '__main__':
    import glob
    

    
    ev = evaluator()
    #If they are not given
    texts,topics,topicids,topicidx = ev.load_topics(sys.argv[1])
    
    
#    print (texts)
#    print (topicids)

    
    counter = ev.analyze(texts, topics,topicids,topicidx)
    print (counter)
