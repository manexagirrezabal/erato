# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

from urllib.parse import urlparse, parse_qs

#https://pythonbasics.org/webserver/
#https://stackoverflow.com/questions/8928730/processing-http-get-input-parameter-on-server-side-in-python
#https://www.w3schools.com/howto/howto_css_two_columns.asp

from main import evaluate_poem

import matplotlib
matplotlib.use("Agg")

from matplotlib import pyplot as plt

from io import BytesIO
import base64

import pandas as pd
import numpy as np

from evaluators import generalSingleEvaluator

gse = generalSingleEvaluator()
gse.initialize_evaluators()
gse.load_model()


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
    print ("-"+data_type+"-")
    if data_type=="stanzacount":
        return "The poem has "+str(data)+" stanzas"
    elif data_type=="linecount":
        return "The poem has "+str(data)+" lines for each stanza"
    elif data_type=="Stresses":
        str_return = "The poem has the following stress pattern<br/>\n"
        for stanza in data:
            for stresses in stanza:
                str_return += stresses + "<br/>\n"
            str_return += "<br/>\n"
        return str_return
    elif data_type == "No. of syllables per line":
        return "The poem has "+str(data)+" syllables per line"
    elif data_type == "rhyme":
        str_return = "The poem has "+str(data['no_rhymes'])+" different rhymes.\n<br/>"
        str_return+= "Rhyme richness is "+str(data['rhymerichness'])
        return str_return
    elif data_type == "intranovelty":
        print (data.values())
#        print ("Plotting")
        plt.clf()
        plt.plot([0.03297652394291049, 0.001221001221001221, 0.0, 0.0, 0.0316836991206739, 0.008679643908673046], color="red", alpha=0.7, label="Sonnet no.18")
        plt.plot([0.03180682529422025, 0.0030642434488588337, 0.0, 0.0, 0.03180682529422025, 0.008976563837231754],color="red",alpha=0.7, label="Sonnet no. 1")
#        plot_openai()
#        plot_poetryme()
        plt.plot(list(data.values()),color="black",label="Current poem")
        plt.xticks(ticks=range(len(data.values())),labels=list(data.keys()))
        plt.legend()
        return ""
    else:
        return str(data_type) + " " + str(data)

hostName = "localhost"
serverPort = 8080

style = '''<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {
  box-sizing: border-box;
}

/* Create two equal columns that floats next to each other */
.column {
  float: left;
  width: 50%;
  padding: 10px;
  height: 600px; /* Should be removed. Only for demonstration */
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}

.drop-zone {
  width: 200px;
  height: 200px;
  border: 2px dashed #ccc;
  padding: 10px;
  text-align: center;
  font-size: 18px;
}
</style>'''

#Helped by ChatGPT
#Addition by https://www.javascripture.com/FileReader and https://www.javascripture.com/FileList
javascript = '''
<script>
const dropZone = document.getElementById('drop-zone1');

dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('highlight');
});

dropZone.addEventListener('dragleave', () => {
  dropZone.classList.remove('highlight');
});

dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('highlight');
  const files = e.dataTransfer.files;
  for (var i = 0; i < files.length; i++) {
      console.log(files[i].name);
      var reader = new FileReader();
      reader.onload = function(){
        var text = reader.result;
        var textarea = document.getElementById("text")
        textarea.innerHTML = text
    };
    reader.readAsText(files[0]);
    }
  // do something with the dropped files
});
</script>
'''

browsefiles = '''
<input id='file-input' type='file' multiple>
<script>
  var fileInput = document.getElementById('file-input');
  fileInput.addEventListener('change', function(event) {
    var input = event.target;

    for (var i = 0; i < input.files.length; i++) {
      console.log(input.files[i].name);
    }
  });
</script>

'''

firstpart = '''<div class="row">
  <div class="column" style="background-color:#aaa;">'''

middlepart = '''  </div>
  <div class="column" style="background-color:#bbb;">'''

lastpart = '''  </div>
</div>'''




class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        imsi = query_components.get("text",['kk'])[0]
        result = analyze(imsi)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        

        self.wfile.write(bytes("<html><head><title>Erato</title>"+style+"</head>", "utf-8"))
#        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))

        self.wfile.write(bytes(firstpart,"utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<form action=\"./\">", "utf-8"))
        self.wfile.write(bytes("<p>Please write a poem that you want to analyze and press the submit button below to analyze</p>", "utf-8"))
        self.wfile.write(bytes("<textarea rows='20' cols='60' id=\"text\" name=\"text\">"+imsi+"</textarea>", "utf-8"))
        self.wfile.write(bytes("<br/>", "utf-8"))
        self.wfile.write(bytes("<div class=\"drop-zone\" id=\"drop-zone1\">Drop files here 1</div>","utf-8"))
#        self.wfile.write(bytes("<div class=\"drop-zone\" id=\"drop-zone2\">Drop files here 2</div>","utf-8"))
#        self.wfile.write(bytes("<div class=\"drop-zone\" id=\"drop-zone3\">Drop files here 3</div>","utf-8"))
        self.wfile.write(bytes("<input type=\"submit\" method=\"post\" value=\"Submit\">", "utf-8"))
        self.wfile.write(bytes("</form>", "utf-8"))

        self.wfile.write(bytes(middlepart,"utf-8"))

        

        for el in result.keys():
            self.wfile.write(bytes("<label>"+print_cute(result[el],el)+"</label>", "utf-8"))
            self.wfile.write(bytes("<br/>", "utf-8"))


        #        plt.plot([1,2,3],[1,2,5])
            if el == "intranovelty":
                with BytesIO() as buffer:
                    plt.savefig(buffer, format="png")
                    encoded = buffer.getvalue()
                    html = '<img src=\'data:image/png;base64,'
                    self.wfile.write(bytes(html, "utf-8"))
                    self.wfile.write(base64.b64encode(encoded))
                    self.wfile.write(bytes("\' width=\"50%\">", "utf-8"))


        self.wfile.write(bytes(lastpart,"utf-8"))

        self.wfile.write(bytes(javascript,"utf-8"))

#        self.wfile.write(bytes("<xml>", "utf-8"))
#        for el in result.keys():
#            self.wfile.write(bytes("<el id=\""+el+"\">"+str(result[el])+"</el>", "utf-8"))
#        self.wfile.write(bytes("</xml>", "utf-8"))

        self.wfile.write(bytes("</body></html>", "utf-8"))

        
#        print (query_components)
        
#        print (change(imsi))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
