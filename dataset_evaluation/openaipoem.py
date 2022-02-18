import os
import openai

f=open("openaikey")
line=f.readline().strip()
f.close()

#openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.api_key = ""
openai.api_key = line

#response = openai.Completion.create(
#  engine="text-davinci-001",
#  prompt="Write a sonnet about virus",
  #prompt="Escribe un soneto sobre virus",
#  temperature=0.7,
#  max_tokens=300,
#  top_p=1,
#  frequency_penalty=0,
#  presence_penalty=0
#)


def get_poem(form,language,seed):
    params = {
        "engine":"text-davinci-001",
#        "prompt:"Write a sonnet about virus",
#        "prompt":"Escribe un soneto sobre virus",
        "temperature":0.7,
        "max_tokens":300,
        "top_p":1,
        "frequency_penalty":0,
        "presence_penalty":0
        }

    if language=="es":
        params['prompt'] = "Escribe un soneto sobre " + seed
    elif language=="en":
        params['prompt'] = "Write a sonnet about " + seed
    
    response = openai.Completion.create(
            engine=params['engine'],
            prompt=params['prompt'],
            temperature=params['temperature'],
            max_tokens=params['max_tokens'],
            top_p=params['top_p'],
            frequency_penalty=params['frequency_penalty'],
            presence_penalty=params['presence_penalty']
            )

    result = response.to_dict_recursive()['choices'][0]['text'].strip()
    return (response.to_dict_recursive(),result, params)

if __name__ == "__main__":
    form     = "sonnet"
    seeds    = "virus"
    language = "es"
#    surprise = "0.005"
    whole_output,text,params = get_poem(form, language,seeds)
    print (text)
