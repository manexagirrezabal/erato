
# Erato: Making it easier to evaluate poetry
This is the repository for Erato, a framework for the automatic evaluation of poetry. It is especially suited for automatic poetry generation models and it provides some automatic tools for the assessment of poetry.

# How to use Erato
It is very easy to use Erato, but it depends on how you want to use it. You can use it from the terminal or with the simple web version that we implemented. The web version is a 

### From the terminal
If you are planning to use Erato from a Unix terminal, you should run the `main.py` program. As it can be seen in the documentation of the script, these are the arguments that you need to use.

```
usage: main.py [-h] [--filename FILENAME] [--directory DIRECTORY] [--list]
Please use this script to evaluate a poem or a collection of poems
optional arguments:
  -h, --help            show this help message and exit
  --filename FILENAME, -f FILENAME
                        The file with the poem you want to analyze
  --directory DIRECTORY, -d DIRECTORY
                        The directory with the poem collection you want to
                        analyze
  --list, -l
```

For example, if we run the program with these arguments, where we analyze [this poem](https://github.com/manexagirrezabal/erato/blob/master/dataset_evaluation/dataset/poetrymeenglish/poems10/poem103.txt):

`python3 main.py -f dataset_evaluation/dataset/poetrymeenglish/poems10/poem103.txt`

We will receive the output of Erato as this dictionary, with the keys `stanzacount`, `linecount`, `No. of syllables per line`, `Stresses`, `rhyme` and `intranovelty`:

`{'stanzacount': 4,`
`'linecount': [4, 4, 4, 2],`
`'No. of syllables per line': [[12, 10, 11, 11], [10, 11, 10, 11], [11, 11, 10, 11], [10, 11]],`
`'Stresses': [['++-+-++--+--', '++-+--+-++', '+-+-+-+-++-', '++--+-+-'], ['++--+-++++', '+--+-+-+-+-', '-+--+++-++', '-++-+-+--+-'], ['+++++--+-+-', '+--+-+--++-', '+-+--++-++', '+--+--+-+++'], ['++-+--++-+', '-+--++++-+-']],`
`'rhyme': {'no_rhymes': 2, 'rhymerichness': 0.2857142857142857},`
`'intranovelty': {'rouge-1': 0.06068588274470623, 'rouge-2': 0.003175133689839572, 'rouge-3': 0.0, 'rouge-4': 0.0, 'rouge-l': 0.054162504162504115, 'rouge-su4': 0.01680527041319828}}`

In the above command, we have analyzed one single poem. There are some analyses that require a set of poems, though. For instance, we can measure how novel are the poems by calculating the ROUGE metric accross different works. If we run the following command, we will get the analysis of a set of poems.

`python3 main.py -d dataset_evaluation/dataset/poetrymeenglish/poems10/`

This will return the individual analyses of each poem included in that directory, in the same format as stated above. But it will also include a general analysis, which looks like this:

`{'acrossnovelty (lbyl, alllines, singlestr)': (array([0.09449386, 0.00674325, 0.00294118, 0.00261438, 0.08578161,
       0.02693924]), array([0.07305423, 0.00499035, 0.00071255, 0.00058952, 0.06585996,
       0.0197717 ]), array([0.34928524, 0.06257612, 0.01186326, 0.00755715, 0.18992304,
       0.12194953]))}`
       
This result includes three arrays, and each array contains six values. The six values are for different types of ROUGE values: ROUGE-1, ROUGE-2, ROUGE-3, ROUGE-4, ROUGE-LCS and ROUGE-SU4, as it was done in Gonçalo Oliveira et al. (2017). The three arrays represent three different ways to calculate the ROUGE overlap (Check section 4.2 in Agirrezabal et al. (2023) or section 5.3 in Gonçalo Oliveira et al. (2017) for further information).

### Web version
If you prefer to use Erato as a simple way to evaluate poems and you want to avoid the terminal as much as possible, you can use the simple web version that we implemented. In order to use this, it is required that Erato is running as a server which can be done by running the following command:

`python3 web_demo_single_simplified.py`

Once that this command is running (make sure that you can read `Server started http://localhost:8080` at the terminal), then there are two ways for using it:

 1.- Open the file called erato_gpt3.html, paste the poem there and press submit
 
 2.- Open the web browser and navigate to the address "http://localhost:8080/". Paste the poem in the text area or drag a text file to the draggable area, and after that, press submit.
 
After that, results will be shown in the right column.

# Current implemented features

### Poetic features
We include the following metrics:
 - stanza counter
 - Line counter
 - Syllable counter
 - A scansion model
 - A rhyme checker (Plecháč, 2018) that checks
    - (1) the number of rhyme patterns
    - (2) the ratio of rhyming lines, or rhyme richness

### Novelty features
We calculate novelty within a single poem and accross poems, using the ROUGE metric.

### Lexico Semantic features
 - Type Token ratio
 - Sentiment analysis (Pérez et al., 2023) based on [pysentimiento](https://github.com/pysentimiento/pysentimiento)

## How to add new features

# Citation
If you find Erato useful for your work, please do cite the work. Here you can find the reference:

 - Agirrezabal, M., Gonçalo Oliveira, H., Ormazabal, A. (2023) Erato: Automatizing Poetry Evaluation, Proceedings of the Portuguese Conference on Artificial Intelligence (EPIA 2023)

You can read the full paper [here](https://arxiv.org/abs/2310.20326).

# References
 - Gonçalo Oliveira, H., Hervás, R., Díaz, A., & Gervás, P. (2017). Multilingual extension and evaluation of a poetry generator. Natural Language Engineering, 23(6), 929-967.
 - Perez, J. M., Rajngewerc, M., Giudici, J. C., Furman, D. A., Luque, F., Alemany, L. A., & Martínez, M. V. (2023). pysentimiento: A Python Toolkit for Opinion Mining and Social NLP tasks.
 - Plecháč, P. (2018). A collocation-driven method of discovering rhymes (in Czech, English, and French poetry). Taming the Corpus: From Inflection and Lexis to Interpretation, 79-95.

# Contact
If you have any trouble running Erato for your own research, please do not hesiitate to contact. Feel very welcome to contact Manex at (manex.agirrezabal@gmail.com).
