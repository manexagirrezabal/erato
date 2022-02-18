
import json
f=open("corpus_poetryme.json")
lines = [json.loads(line) for line in f]
f.close()

for indline,line in enumerate(lines):
    print ("POEM ",indline, line['language'], line['seeds'])
    print (line['text'].strip())
    print ()
