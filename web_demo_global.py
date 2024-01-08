# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from urllib.parse import urlparse, parse_qs

from io import BytesIO
import base64

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt

from main import evaluate_poem
from evaluators import generalSingleEvaluator
gse = generalSingleEvaluator()
gse.initialize_evaluators()
gse.load_model()

from tqdm import tqdm

import re

global subplot_idx


#https://pythonbasics.org/webserver/
#https://stackoverflow.com/questions/8928730/processing-http-get-input-parameter-on-server-side-in-python
#https://www.w3schools.com/howto/howto_css_two_columns.asp


def conv(cell):
    return np.array(cell[1:-1].split(","),dtype=float)


intrasoai = pd.read_csv("models/lindep/openai_eng_all_intras.tsv",sep="\t", header=None)
intraoaivalues = intrasoai.loc[:,1].map(conv)
intrasptm = pd.read_csv("models/lindep/poetryme_eng_all_intras.tsv",sep="\t", header=None)
intraptmvalues = intrasptm.loc[:,1].map(conv)

def plot_openai():
    for values in intraoaivalues:
        plt.plot(values, alpha=0.05,color="blue")

def plot_poetryme():
    for values in intraptmvalues:
        plt.plot(values, alpha=0.05,color="green")

def analyze(st):
    poemlines = st.split("\r\n")

    res, lines= gse.analyze_lines(poemlines)

    return res

def print_cute(data, data_type):
    global subplot_idx

    print ("-"+data_type+"-")
    if data_type=="stanzacount":
        return "The poem has "+str(data)+" stanzas"
    elif data_type=="linecount":
        return "The poem has "+str(data)+" lines for each stanza"
    elif data_type=="Stresses":
        str_return = "The poem has the following stress pattern<br/>\n"
        print (data)
        max_sylls = max([len(el) for stanza in data for el in stanza])
        def get_stress (scansion_line,idx):
            if idx < len(scansion_line):
                if scansion_line[idx]=="+":
                    return 1
            return 0
        toplot = [sum([get_stress(line,syllno) for stanza in data for line in stanza]) for syllno in range(max_sylls)]

        plt.subplot(3,1,subplot_idx)
        plt.plot(toplot)
        subplot_idx=subplot_idx+1

        str_return = ""

        #If we want to print the whole table, this is done with the code below
#        str_return += "<table>"
#        str_return += "<tr>"
#        for val in toplot:
#            str_return += "<td>"+str(val)+"</td>"
#        str_return += "</tr>"
#        for stanza in data:
#            str_return += "<tr><td></td></tr>"
#            for stresses in stanza:
#                str_return += "<tr>"
#                for stress in stresses:
#                    str_return += "<td>"+stress + "</td>"
#                str_return += "</tr>"
#            str_return += "<tr></tr>"
#        str_return += "</table><br/><br/>"
        return str_return



    elif data_type == "No. of syllables per line":

        plt.subplot(3,1,subplot_idx)
        plt.boxplot(data)
        subplot_idx=subplot_idx+1


        return "The poem has "+str(data)+" syllables per line"
    elif data_type == "rhyme":
        str_return = "The poem has "+str(data['no_rhymes'])+" different rhymes.\n<br/>"
        str_return+= "Rhyme richness is "+("%.3f" % data['rhymerichness'])
        return str_return
    elif data_type == "intranovelty":
        plt.subplot(3,1,subplot_idx)
        print (data.values())
#        print ("Plotting")
        
        plt.plot([0.03297652394291049, 0.001221001221001221, 0.0, 0.0, 0.0316836991206739, 0.008679643908673046], color="red", alpha=0.7, label="Sonnet no.18")
        plt.plot([0.03180682529422025, 0.0030642434488588337, 0.0, 0.0, 0.03180682529422025, 0.008976563837231754],color="red",alpha=0.7, label="Sonnet no. 1")
#        plot_openai()
#        plot_poetryme()
        plt.plot(list(data.values()),color="black",label="Current poem")
        plt.xticks(ticks=range(len(data.values())),labels=list(data.keys()))
        plt.legend()
        subplot_idx=subplot_idx+1
        return ""
    else:
        return str(data_type) + " " + str(data)

hostName = "localhost"
serverPort = 8080

f=open("eratogroup_htmlcontent_gpt3enhanced.html")
all_file = f.read().split("##########")
f.close()


firstpart  = all_file[0]
secondpart = all_file[1]
lastpart   = all_file[2]


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global subplot_idx

        query_components = parse_qs(urlparse(self.path).query)
        imsi = query_components.get("text",['kk'])[0]
        if imsi != "kk":
            result = analyze(imsi)
        else:
            result = {}

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'localhost')
        self.send_header("Content-type", "text/html")
        self.end_headers()
        


        self.wfile.write(bytes(firstpart,"utf-8"))

#        self.wfile.write(bytes("<div id=\"text\" name=\"text\" style=\"display:None\">"+imsi+"</div>", "utf-8"))
        self.wfile.write(bytes("<div id=\"text\" name=\"text\">"+imsi+"</div>", "utf-8"))

        self.wfile.write(bytes(secondpart,"utf-8"))


        plt.clf()
        plt.subplots(nrows=3)
        subplot_idx=1
        for el in result.keys():
            self.wfile.write(bytes("<label>"+print_cute(result[el],el)+"</label>", "utf-8"))
            self.wfile.write(bytes("<br/><br/>", "utf-8"))

        #        plt.plot([1,2,3],[1,2,5])
        if subplot_idx>1:
            with BytesIO() as buffer:
                plt.savefig(buffer, format="png")
                encoded = buffer.getvalue()
                html = '<img src=\'data:image/png;base64,'
                self.wfile.write(bytes(html, "utf-8"))
                self.wfile.write(base64.b64encode(encoded))
                self.wfile.write(bytes("\' width=\"50%\">", "utf-8"))

        self.wfile.write(bytes(lastpart,"utf-8"))


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
