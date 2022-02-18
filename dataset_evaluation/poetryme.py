
#Poetryme Rest Api example
#https://poetryme.dei.uc.pt/PoetrymeWeb/rest/poetry?lang=en&form=sonnet&seeds=love&surp=0.001

#Following this: https://www.delftstack.com/howto/python/python-get-json-from-url/

import requests, json




def get_poem(form,language,seeds,surprise):
    url = requests.get("http://poetryme.dei.uc.pt/PoetrymeWeb/rest/poetry?lang="+language+"&form="+form+"&seeds="+seeds+"&surp="+surprise,verify=False)
    text = url.text
    data = json.loads(text)
    return data

if __name__ == "__main__":
    language = "en"
    form     = "sonnet"
    seeds    = "virus"
    surprise = "0.005"
    result = get_poem(form, language,seeds,surprise)
    print (result['text'])
