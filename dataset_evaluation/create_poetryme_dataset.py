
import warnings
warnings.filterwarnings("ignore")
import datetime
ct = str(datetime.datetime.now()).replace(" ","_")

import json

from poetryme import get_poem
form     = "sonnet"
surprise = "0.005"

howmany = 10
languages = "en es".split(" ")
seeds={}
seeds['es']  = "amor artificial azul cantar ordenador construir futbol leer nuevo poesía virus pandemia mascarilla".split(" ")
seeds['en']  = "love artificial blue sing computer build football read new poetry virus pandemic facemask".split(" ")
fp = open("corpus"+ct, "w")
for language in languages:
    print (language)
    for seed in seeds[language]:
        for n in range(howmany):
            data = get_poem(form,language,seed,surprise)
            print (data['text'])
            json.dump(data,fp)
            fp.write("\n")
    print ()
fp.close()
