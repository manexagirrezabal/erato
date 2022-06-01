
#conda activate poetryevaluation

#import pandas as pd
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import numpy as np

from matplotlib import pyplot as plt
        
from sklearn.metrics import classification_report,f1_score

import sys

#Downloaded topic dataset from https://www.kaggle.com/datasets/michaelarman/poemsdataset
#Exported it to the right format with
#python3 format_poemsdataset.py /Users/jbt694/corpusak/poetry/poemsdataset/topics


def cosine_similarity(v1, v2):
    return np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))

#NLI model
#DISTILBERT_BASE_NLI='sentence-transformers/distilbert-base-nli-stsb-mean-tokens'

#The first one works way better in my examples
#extractor = SentenceTransformer(DISTILBERT_BASE_NLI) #only works for sentence transformers


#BERT model
#BERT_BASE_UNCASED='bert-base-uncased'
#BERT_BASE_UNCASED='mrm8488/RoBasquERTa'


#SYSTEM 1
#BERT_BASE_UNCASED='dccuchile/bert-base-spanish-wwm-uncased'
#extractor = pipeline('feature-extraction', model=BERT_BASE_UNCASED)

#def get_representation(text):
#    return np.array(extractor(text)[0][1:-1]).mean(axis=0)


#SYSTEM 2
#model = SentenceTransformer('hiiamsid/sentence_similarity_spanish_es')
#get_representation = model.encode


#SYSTEM 3 (the best so far)
model = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v1')
get_representation = model.encode


#I have a gut feeling that this is going to work well
#from transformers import AutoTokenizer, AutoModelForSequenceClassification
#tokenizer = AutoTokenizer.from_pretrained("Recognai/bert-base-spanish-wwm-cased-xnli")
#model = AutoModelForSequenceClassification.from_pretrained("Recognai/bert-base-spanish-wwm-cased-xnli")


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
#                topics.append(bertsoaldi)
                topics.append(topic)
    
        #If the topic is a directory name, convert them to a readable number
        topics_v = sorted(set(topics))
        notopics = len(topics_v)
        topic_idx = {topic:idx for idx,topic in enumerate(topics_v)}
        topicids = [topic_idx[topic] for topic in topics]
        print ("topic_idx",topic_idx)

        return texts,topics,topicids,topic_idx
        
    @staticmethod
    def analyze(texts, topics,topicids,topicidx):
        """
        param texts: This a list with the texts we want to analyze
        The keys are the same as the analyses

        The program returns three cross-poem metrics
        """

        idx2topic = {topicidx[topic]:topic for topic in topicidx.keys()}
        print ("idx2topic",idx2topic)
        topicv=list(sorted(idx2topic.keys()))
        distances = np.zeros((len(texts),len(topicv)))
        for indtext,text in enumerate(texts):
            for indtopic,topic in enumerate(topicv):
                textrep = get_representation(text)
                topicrep = get_representation(idx2topic[topic])

                #Instead of encoding the whole poem as such,
                #calculate similarities between the topic and each poem line (verse)
                #and calculate the average cosine distance
                #Maybe min/max cosine distance?
                
 #               print ("HELLO")
 #               print (indtext,indtopic)
 #               print (cosine_similarity(textrep,topicrep))
                print (idx2topic[topic])
                print (text)
                distances[indtext][indtopic] = cosine_similarity(textrep,topicrep)
                print (distances[indtext][indtopic])
                print (indtext,indtopic,distances.shape)
                print ()

        #For each topic, look for the N closest poems
        n = int(distances.shape[0]/distances.shape[1])
        predicted_topn={}
        for indtopic,topic in enumerate(topicv):
            #Argsort sorts from small to big
            #Meaning that the index that is at the end is the most related poem
            #print (indtopic,np.min(distances[:,indtopic]),np.max(distances[:,indtopic]),np.argsort(distances[:,indtopic]))
            predicted_topn[topic] = np.argsort(distances[:,indtopic])[-n:]

        true_topn = {topic:np.argwhere(topicids==topic).reshape(-1) for topic in topicv}

        print ("RESULTS!")
        for topic in predicted_topn.keys():
            print (topic,predicted_topn[topic],true_topn[topic])
            predicted_relevant_documents = set(predicted_topn[topic]).intersection(true_topn[topic])
            print (predicted_relevant_documents)
            if len(predicted_topn[topic])==0:
                precisioin=0
            else:
                precision = len(predicted_relevant_documents)/len(predicted_topn[topic])
            if len(true_topn[topic])==0:
                recall=0
            else:
                recall    = len(predicted_relevant_documents)/len(true_topn[topic])
            if precision==0 and recall==0:
                f1score=0
            else:
                f1score = (2 * precision * recall) / (precision + recall)
    
            print (precision,recall,f1score)


        predicted_topicids = np.array(np.argmax(distances,axis=1),dtype=int)
        predicted_topics = [idx2topic[el] for el in predicted_topicids]
        
        
        print ("Actual topics",topics)
        print ("Actual topic ids",topicids)
        print ()
        print ("Recall analysis")
        print ("Topic idx (dictionary)",topicidx) #Topic dictionary
        print ("Top N predicted elements for each topic (N = ndocs/ntopics)",predicted_topn)
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
