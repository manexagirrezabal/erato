
### Semantic model evaluation

I tested three different models for computing the similarity between the topics and the poems themselves:

1.- dccuchile/bert-base-spanish-wwm-uncased: 
Performance measures here: https://github.com/manexagirrezabal/erato/blob/master/testing_directory/semantic_test_poetryme_spanish.txt

2.- hiiamsid/sentence_similarity_spanish_es:
Performance measures here: https://github.com/manexagirrezabal/erato/blob/master/testing_directory/sentence_similarity_spanishModel-poetrymespanish.txt

3.- sentence-transformers/distiluse-base-multilingual-cased-v1:
Performance measures here: https://github.com/manexagirrezabal/erato/blob/master/testing_directory/sentence_transformers.txt


Further ideas

Some ideas.

I think that we can follow an approach that is similar to UDPIPE, Ixapipes or Stanford CoreNLP.

First we perform single evaluation procedures.

Afterwards, we can do evaluation accross poems.

#### The framework

1.- Poetic features: Conformance of metre

Ignore/just count-inform/evaluate (In the future, suggest metre)

 1.1.- stanzas

 1.2.- No. syllables:
 Average deviation of expected number of syllables per line (Mean Average Error)
 When ambiguity is allowed, consider the best case.

1.3.- rhymes:
https://github.com/versotym/rhymeTagger
https://github.com/sravanareddy/rhymedata
https://github.com/jvamvas/rhymediscovery
Rhyme accuracy. E.g.

'''
A waste
B berry
A poltergeist
B cherry
C land
D peter
E tom
E pim
E lord
4/7 rhymes are correct
'''

For each stanza, we have to check the rhyme pattern. If the rhyme letter (A,B,C,D,E) appears more than once, we consider as a rhyming element.

'''
If there are two letters in the stanza (A,A),
if both lines rhyme -> 1
else -> 0
'''

'''
If there are three letters in the stanza (E,E,E),
if the three words rhyme -> 1
if 2/3 words rhyme ->0.5
if none rhymes -> 0
'''

'''
If there are N letters in the stanza (T1,T2, ..., TN),
if there are N words that rhyme -> 1
N-1 words that rhyme 1-(1/(N-1))
N-2 words that rhyme 1-(2/(N-1))
N-k words that rhyme 1-(k/(N-1))
if there are zero words (1/N) that rhyme -> 0
'''

Tested software for rhymes:
-Dopelearning, rhyme density
https://github.com/ekQ/raplysaattori.git
cd /Users/jbt694/project_poetryevaluation/erato/testing_directory/raplysaattori
/opt/anaconda3/envs/glample/bin/python2.7 raplyzer.py
This returns us the rhyme density, but this is calculated as multisyllabic assonance, and not proper rhyme
If we are desperate, we could use that (it returns a number that could be used to compare across different models and
even with rappers)



1.4.- stresses
Following my thesis, inspired by Manurung
https://www.tandfonline.com/doi/pdf/10.1080/0952813X.2010.539029

MED distance, like in my thesis, pg. 105
accuracy = 1 - (MED(gold,pred)/(max(len(gold),len(pred))))


2.- Lexical and semantic (topic related) features

2.1.- type token ratio, considering only content words + Lexical repetition
2.2.- Word frequency distribution (Jurafsky and Kao, 2012)
1.and
2.the
3.a
345.house
346.window
...
Ranking based on the frequency. For a given poem, return the frequency ranking of each word. The lower the number the more unfrequent words they are. If word is not in the dictionary, count.
2.3.- Topicality as a retrieval problem (multipoetryme, word2vec, doc2vec, BERT)
2.4.- LDA idea

Retrieval problem

For this evaluation, we would expect to have 90 sonnets.

10 seed words (topics), 3 polarities, 3 poems for each polarity

 1.- They filter stop words from poems.

 2.- They calculate the average PPMI distance between the seed word and each word in each poem

      Instead of using PPMI, we can use pretrained word embeddings (some established embeddings)

 3.- Get the top 9 closest poems, and see whether those 9 are the ones that are about the seed word

'''
      If none of them is among the top 9, return 0
      If all of them are among the top 9, return 1
      and I guess that all others are values in between
'''

3.-Novelty

3.1.-Itself:Structure variation, as in Poetryme. 4 ROUGE measures

3.2.- Plagiarism check

Initial system: Check whether the generated lines are in the training corpus.

Future work: Use a proper plagiarism system, Google search, Twitter search, and so on.


4.- Poetic fluency
SoA LM based probability. Compare regular text vs gold standard poetry
The expectation would be that poetry should resemble more poetry




#### How to make it language independent:

1.-
Rhymes: https://www.aclweb.org/anthology/P11-2014/

2.-

3.-


#### What do we need for each language?
For instance, English:

1.-

2.-

3.-

#### Ideas for the future
I think that Rouge is really good to measure the intra novelty.
If poetry should sound similar, I would expect that a character-level rouge measure would give us a metric
 of how similar letters/letter n-grams are used. And I would expect some sort of repetition, assuming that
 alliteration/similar sounds do happen in poetry
Then, maybe analyzing the ratio between the word-based rouge and the character-based rouge could be a good metric.
