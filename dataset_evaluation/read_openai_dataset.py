
import json
f=open("corpus_openai.json")
lines = [json.loads(line) for line in f]
f.close()

for indline,line in enumerate(lines):
    print ("POEM ",indline, line['prompt'])
    print (line['choices'][0]['text'].strip())
    print ()
