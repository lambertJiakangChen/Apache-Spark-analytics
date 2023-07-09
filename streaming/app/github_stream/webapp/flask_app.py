"""
    This Flask web app provides a very simple dashboard to visualize the statistics sent by the spark app.
    The web app is listening on port 5000.
    All apps are designed to be run in Docker containers.
    
    Made for: EECS 4415 - Big Data Systems (Department of Electrical Engineering and Computer Science, York University)
    Author: Changyuan Lin

"""


from flask import Flask, jsonify, request, render_template
from redis import Redis
import matplotlib.pyplot as plt
import json
import pandas as pd

app = Flask(__name__)

@app.route('/updateData', methods=['POST'])
def updateData():
    data = request.get_json()
    r = Redis(host='redis', port=6379)
    r.set('data', json.dumps(data))
    return jsonify({'msg': 'success'})

@app.route('/push_change', methods=['POST'])
def push_change():
    datacha = request.get_json()
    r = Redis(host='redis', port=6379)
    r.set('datacha', json.dumps(datacha))
    return jsonify({'msg': 'success'})

@app.route('/star_avg', methods=['POST'])
def star_avg():
    datastar = request.get_json()
    r = Redis(host='redis', port=6379)
    r.set('datastar', json.dumps(datastar))
    return jsonify({'msg': 'success'})


@app.route('/Pythonword', methods=['POST'])
def Pythonword():
    data1 = request.get_json()
    r = Redis(host='redis', port=6379)
    r.set('data1', json.dumps(data1))
    return jsonify({'msg': 'success'})

@app.route('/Csharpword', methods=['POST'])
def Csharpword():
    data2 = request.get_json()
    r = Redis(host='redis', port=6379)
    r.set('data2', json.dumps(data2))
    return jsonify({'msg': 'success'})

@app.route('/Javaword', methods=['POST'])
def Javaword():
    data3 = request.get_json()
    r = Redis(host='redis', port=6379)
    r.set('data3', json.dumps(data3))
    return jsonify({'msg': 'success'})

py_list=[]
ja_list=[]
cs_list=[]
time = []

@app.route('/', methods=['GET'])
def index():
    r = Redis(host='redis', port=6379)
    data = r.get('data')
    datacha = r.get('datacha')
    datastar = r.get('datastar')
    data1 = r.get('data1')
    data2 = r.get('data2')
    data3 = r.get('data3')

    try:
        data = json.loads(data)
    except TypeError:
        return "waiting for data..."
    try:
        datacha = json.loads(datacha)
    except TypeError:
        return "waiting for datacha..."
    try:
        datastar = json.loads(datastar)
    except TypeError:
        return "waiting for datastar..."
    
    try:
        data1 = json.loads(data1)
    except TypeError:
        return "waiting for data1..."
    
    try:
        data2 = json.loads(data2)
    except TypeError:
        return "waiting for data2..."
    
    try:
        data3 = json.loads(data3)
    except TypeError:
        return "waiting for data3..."
    # 4i
    try:
        py_index = data['language'].index('Python')
        Python = data['count'][py_index]
    except ValueError:
        Python = 0
    try:
        ja_index = data['language'].index('Java')
        Java = data['count'][ja_index]
    except ValueError:
        Java = 0
    try:
        cs_index = data['language'].index('C#')
        CSharp = data['count'][cs_index]
    except ValueError:
        CSharp = 0
    
    # 4ii
    try:
        C_time = datacha['C_time'][1]
        time.append(C_time)
    except ValueError:
        C_time = 0
    if len(time) == 7:
        time.pop(0)

    try:
        py_index1 = datacha['language'].index('Python')
        Pythoncha = datacha['count'][py_index1]
        py_list.append(Pythoncha)
    except ValueError:
        Pythoncha = 0
    if len(py_list) == 7:
        py_list.pop(0)

    try:
        ja_index1 = datacha['language'].index('Java')
        Javacha = datacha['count'][ja_index1]
        ja_list.append(Javacha)
    except ValueError:
        Javacha = 0
    if len(ja_list) == 7:
        ja_list.pop(0)

    try:
        cs_index1 = datacha['language'].index('C#')
        CSharpcha = datacha['count'][cs_index1]
        cs_list.append(CSharpcha)
    except ValueError:
        CSharpcha = 0
    if len(cs_list) == 7:
        cs_list.pop(0)
 
    f = plt.figure(1)
    pytime = pd.DataFrame({'Time': time, 'classes': py_list})
    jatime = pd.DataFrame({'Time': time, 'classes': ja_list})
    cstime = pd.DataFrame({'Time': time, 'classes': cs_list})
    line1 = plt.plot(pytime.Time, pytime.classes, color = "red")
    line2 = plt.plot(jatime.Time, jatime.classes, color ='blue')
    line3 = plt.plot(cstime.Time, cstime.classes, color ='yellow')
    plt.xticks(rotation=30, ha='right')
    plt.xlabel('Time')
    plt.ylabel('#repository')
    plt.legend([line1, line2, line3], ['Python', 'Java', 'CSsharp'])
    f.savefig('/app/github_stream/webapp/static/images/chart.png')

    # 4iv
    pydict = {}
    for x in data1['Pythonwords']:
        w_index = data1['Pythonwords'].index(x)
        pydict[x] = data1['count'][w_index]

    CSdict = {}
    for x in data2['CSharpwords']:
        w_index = data2['CSharpwords'].index(x)
        CSdict[x] = data2['count'][w_index]

    Jadict = {}
    for x in data3['Javawords']:
        w_index = data3['Javawords'].index(x)
        Jadict[x] = data3['count'][w_index]
    
    # 4iii
    star_avg_dict = {}
    try:
        py_index = datastar['language'].index('Python')
        Pythonstar = datastar['star_average'][py_index]
        star_avg_dict["Python"] = Pythonstar
    except ValueError:
        Pythonstar = 0
    try:
        ja_index = datastar['language'].index('Java')
        Javastar = datastar['star_average'][ja_index]
        star_avg_dict["Java"] = Javastar
    except ValueError:
        Javastar = 0
    try:
        cs_index = datastar['language'].index('C#')
        CSharpstar = datastar['star_average'][cs_index]
        star_avg_dict["CSharp"] = CSharpstar
    except ValueError:
        CSharpstar = 0
        
    star_lang = list(star_avg_dict.keys())
    star_values = list(star_avg_dict.values())      
    g = plt.figure(2)
    plt.bar(star_lang, star_values, color=['tab:orange', 'tab:grey', 'tab:red'], width = 0.8)
    plt.ylabel('Average number of stars')
    plt.xlabel('PL')
    g.savefig('/app/github_stream/webapp/static/images/chart1.png')
    return render_template('index.html', url='/static/images/chart.png', url1='/static/images/chart1.png', stardic = star_avg_dict, Python=Python, Java=Java, CSharp=CSharp, pywordcount = {k: pydict[k] for k in list(pydict)[:10]}, CSwordcount = {k: CSdict[k] for k in list(CSdict)[:10]}, Jawordcount = {k: Jadict[k] for k in list(Jadict)[:10]})

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
