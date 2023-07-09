import socket
import time
import requests
import os
import re
import random

token = os.getenv('TOKEN')
TCP_IP = "0.0.0.0"
TCP_PORT = 9999
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")
# if the connection is accepted, proceed
conn, addr = s.accept()
print("Connected... Starting sending data.")
n=0
fn_list = []
while True:
    try:
        # url = 'https://api.github.com/search/repositories?q=+language:Java+language:JavaScript+language:Python&sort=updated&order=desc&per_page=50'
        # res = requests.get(url, headers={"Authorization": token})
        print(token)
        url = 'https://api.github.com/search/repositories?q=+language:Java&sort=updated&order=desc&per_page=50'
        res = requests.get(url, headers={"Authorization": token}).json()
        url1 = 'https://api.github.com/search/repositories?q=+language:Python&sort=updated&order=desc&per_page=50'
        res1 = requests.get(url1, headers={"Authorization": token}).json()
        url2 = 'https://api.github.com/search/repositories?q=+language:CSharp&sort=updated&order=desc&per_page=50'
        res2 = requests.get(url2, headers={"Authorization": token}).json()
        if "items" in res:
            a = res["items"]
        if "items" in res1:
            b = res1["items"]
        if "items" in res2:
            c = res2["items"]
        g =  a + b + c
        repository = (sorted(g, key=lambda x: x['pushed_at'], reverse=True))
        for item in repository:
            if item["language"] is not None:
                if item["full_name"] not in fn_list:
                    fn_list.append(item["full_name"]) 
                    lan = item["language"]
                    stars = item["stargazers_count"]
                    if item["description"] is not None:
                        des = re.sub('[^a-zA-Z ]', '', item["description"])
                    else:
                        des = " "
                    data = f"{lan},{stars},{des}\n".encode()
                    conn.send(data)
                    print(data)
        n=n+1
        if n >= 4:
            fn_list = []
            n=0
        # number = random.randint(1, 1000000000)
        # data = f"{number}\n".encode()
        # conn.send(data)
        # print(number)
        time.sleep(15)
    except KeyboardInterrupt:
        s.shutdown(socket.SHUT_RD)
