from flask import Flask,request
from flask_cors import CORS
import ast
import time
from sementic_search import search
import json
from yt_transcript import yt_search

app = Flask(__name__)
CORS(app)

req_list = []

@app.route('/text',methods=['POST'])
def s_text():
    current_time = time.time()
    req_list.append(current_time)
    if (len(req_list) > 1 and current_time-req_list[-2] > 0.9) or len(req_list) == 1:
        data = request.data
        data = json.loads(data)['query']
        url = data['url']    
        query = data['msgObj']
        result = search(url,query)
        print("In if: ",result)
        return result
    else:
        data = request.data
        data = ast.literal_eval(str(data))
        #print(data)
        #print("In else")
        return "none"

@app.route('/yt',methods=['POST'])
def s_yt():
    current_time = time.time()
    req_list.append(current_time)
    if (len(req_list) > 1 and current_time-req_list[-2] > 0.9) or len(req_list) == 1:
        data = request.data
        data = json.loads(data)['query']
        url = data['url']    
        query = data['msgObj']
        result = yt_search(url,query)
        print("In if: ",data)
        return result
    else:
        data = request.data
        data = ast.literal_eval(str(data))
        #print(data)
        #print("In else")
        return "none"

if __name__ == '__main__':
   app.run()