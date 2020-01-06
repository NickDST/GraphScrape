from flask import Flask, jsonify, render_template, request
from io import StringIO
import pandas as pd
import requests



app = Flask(__name__)

def convertFormat(dfs):
    payload = []
    for df in dfs:
        each_df_payload = []
        columns = df.columns

        for i in range(len(df)):
            dictVal = {}
            for j in range(len(columns)):
                try: 
                    dictVal[str(columns[j])] = int(df[columns[j]][i])
                except:
                    dictVal[str(columns[j])] = str(df[columns[j]][i])
            each_df_payload.append(dictVal)
        payload.append({"columns" : list(columns), "data": each_df_payload})

    return payload


def scraper(link):
    print("scraping...", link)

    try:
        source = requests.get(link).text
        TESTDATA =  StringIO(source)
        df = pd.read_csv(TESTDATA, sep=",")

        if(len(df.columns) > 0 and len(df) > 0):
            print("VALID CSV FORMAT")
            return convertFormat([df])
        
    except:
        print("NOT CSV FORMAT")


    try:
        dfs = pd.read_html(link)
        return convertFormat(dfs)
    except:
        print("no tables found")
        return "No Tables Found"




@app.route('/')
def hello_world():
    return render_template('file.html', someVal = "Hello World")



@app.route('/ScrapeData', methods=['GET'])
def ScrapeData():
    link = request.args.get("submitted_link")
    data = scraper(link)
    return jsonify(data)


# Sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
        return jsonify("yeet")



# run Flask app
if __name__ == "__main__":
    app.run(debug=True)