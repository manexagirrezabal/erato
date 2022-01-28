
Framework
1.- Poetic features: Conformance of metre
Ignore/just count-inform/evaluate (In the future, suggest metre)
- stanzas
- No. syllables:
 Average deviation of expected number of syllables per line (Mean Average Error)
 When ambiguity is allowed, consider the best case.
- rhymes:
Rhyme accuracy. E.g.
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

For each stanza, we have to check the rhyme pattern. If the rhyme letter (A,B,C,D,E) appears more than once, we consider as a rhyming element.

If there are two letters in the stanza (A,A),
if both lines rhyme -> 1
else -> 0

If there are three letters in the stanza (E,E,E),
if the three words rhyme -> 1
if 2/3 words rhyme ->0.5
if none rhymes -> 0

If there are N letters in the stanza (T1,T2, ..., TN),
if there are N words that rhyme -> 1
N-1 words that rhyme 1-(1/(N-1))
N-2 words that rhyme 1-(2/(N-1))
N-k words that rhyme 1-(k/(N-1))
if there are zero words (1/N) that rhyme -> 0

- stresses
Following my thesis, inspired by Manurung
https://www.tandfonline.com/doi/pdf/10.1080/0952813X.2010.539029
MED distance, like in my thesis, pg. 105
accuracy = 1 - (MED(gold,pred)/(max(len(gold),len(pred))))


2.- Lexical and semantic (topic related) features
-type token ratio, considering only content words + Lexical repetition
-Word frequency distribution (Jurafsky and Kao, 2012)
-Topicality as a retrieval problem (multipoetryme, word2vec, doc2vec, BERT)
-LDA idea

Retrieval problem

For this evaluation, we would expect to have 90 sonnets.

10 seed words (topics), 3 polarities, 3 poems for each polarity

 1.- They filter stop words from poems.

 2.- They calculate the average PPMI distance between the seed word and each word in each poem

      Instead of using PPMI, we can use pretrained word embeddings (some established embeddings)

 3.- Get the top 9 closest poems, and see whether those 9 are the ones that are about the seed word

      If none of them is among the top 9, return 0
      If all of them are among the top 9, return 1
      and I guess that all others are values in between


3.-Novelty
3.1.-Itself:Structure variation, as in Poetryme. 4 ROUGE measures
For rouge, I would use this:
https://pypi.org/project/rouge-score/
Because they do not remove stop words.
By now, I will use the python package called rouge_score, and we will
not use rouge-su-4, as it looks complicated.


3.2.- Plagiarism check
Initial system: Check whether the generated lines are in the training corpus.
Future work: Use a proper plagiarism system, Google search, Twitter search, and so on.


4.- Poetic fluency
SoA LM based probability. Compare regular text vs gold standard poetry
The expectation would be that poetry should resemble more poetry




Language independent:
1.-
Rhymes: https://www.aclweb.org/anthology/P11-2014/
2.-
3.-


English:
1.-
2.-
3.-
