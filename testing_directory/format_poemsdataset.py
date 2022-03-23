
import sys
import os

import glob
import shutil

POEMSDIR = sys.argv[1]

for indtopic,direct in enumerate(glob.glob(POEMSDIR+"/*")):
    print (direct)

    topic = direct.split("/")[-1]

    outdir = "output/poems"+str(indtopic)
    os.mkdir(outdir)

    f=open("output/topic"+str(indtopic)+".txt","w")
    f.write(topic)
    f.close()
    
    for indpoem,poemfile in enumerate(glob.glob(direct+"/*.txt")):
#        print (poemfile)
#        print (outdir+"/"+str(indpoem)+".txt")
        shutil.copyfile(poemfile, outdir+"/"+str(indpoem)+".txt")

    
