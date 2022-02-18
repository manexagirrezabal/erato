
#import warnings
#warnings.filterwarnings("ignore")
import datetime
ct = str(datetime.datetime.now()).replace(" ","_")

import json
def Merge(dict1, dict2):
    return(dict2.update(dict1))

from openaipoem import get_poem

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
            whole_output,text,params = get_poem("sonnet",language,seed)
            Merge(params,whole_output)
            print (text)
            json.dump(whole_output,fp)
            fp.write("\n")
    print ()
fp.close()
