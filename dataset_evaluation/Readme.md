
## Computer-generated poetry

The API of PoetryMe and OpenAi was used to generate a set of poems.

Here it is the list of words that we used to generate poems in PoetryMe and OpenAI:

 * amor, love
 * artificial, artificial
 * azul, blue
 * cantar, sing
 * ordenador, computer
 * construir, build
 * futbol, football
 * leer, read
 * nuevo, new
 * poesía, poetry
 * virus, virus
 * pandemia, pandemic
 * mascarilla, facemask

The seedwords are the same words used in the Oliveira et al. (2017) paper, apart from the last three words, which were added out of curiosity to see how the models behave with current topics.

We generated 10 poems for each seed word and for each language.


#### API PoeTryMe
https://drops.dagstuhl.de/opus/volltexte/2017/7946/pdf/OASIcs-SLATE-2017-12.pdf

Further information about PoeTryMe
"PoeTryMe: a versatile platform for poetry generation"
"Multilingual extension and evaluation of a poetry generator"
https://www.sciencedirect.com/science/article/pii/S138904171730311X



## Human poetry

The strategy for creating this data set was a bit trickier in order to get something that would be relatively similar to what we have with the computer generated poems. The most important concern here was semantics (but also meter, to a lesser degree).

In Spanish, we followed the conclusions of Colorado (2015)[1], who created the Corpus of the Golden Age Sonnets[1][2]. They used Topic modeling and they found several clusters of different authors. We used the first three author clusters that they mention (the remaining were avoided because more authors were involved and collecting + organizing all those works would be a bit tedious). We used this corpus[2] instead of the Disco, because some authors of the analysis by Colorado (2015)[1] were missing in the Disco corpus.
 
In the case of English, we decided to create a corpus with three authors that have a rather particular style. The authors are William Shakespeare[3], Edgar Allan Poe[4] and Emily Dickinson[5].

https://www.emilydickinsonmuseum.org/emily-dickinson/poetry/tips-for-reading/major-characteristics-of-dickinsons-poetry/
https://www.gale.com/open-access/edgar-allan-poe
https://www.bl.uk/works/shakespeares-sonnets


[1] https://aclanthology.org/W15-0712.pdf
[2] https://github.com/bncolorado/CorpusSonetosSigloDeOro
[3] https://www.gutenberg.org/ebooks/1041
[4] https://www.gutenberg.org/ebooks/10031
[5] https://www.gutenberg.org/ebooks/12242/