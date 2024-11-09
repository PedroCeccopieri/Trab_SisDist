import socket as st
import random as rd
from threading import Thread

fun = ['som', 'sub', 'mul', 'div']
threads = []

def sendMsg(msg, ip, port):

    sock = st.socket(st.AF_INET, st.SOCK_STREAM)
    sock.connect((ip, port))

    try: 
        sock.send(msg.encode('utf-8'))        
        data = sock.recv(1024)
        return data.decode("UTF-8")

    except st.error as e:
        print ("Socket error: %s" %str(e))

    except Exception as e: 
        print ("Other exception: %s" %str(e))

    finally: 
        print ("Closing connection to the server") 
        sock.close()

def runTest(conections):

    for i in range(conections):
        msg = f'{rd.choice(fun)} {rd.randint(1,10)} {rd.randint(1,10)}'
        t = Thread(target=sendMsg, args= (msg, 'localhost', 5555))
        t.start()
        threads.append(t)

    for i in threads:
        i.join()

    with open("log.txt", 'r') as f:
        s = [i[:-1] for i in f]
        di = {x : s.count(x) for x in set(s)}
        print(di)

        for i, j in di.items():
            print(f"server {i}: {j}")
        print(f"total conections {sum([j for i,j in di.items()])}")

    print('DONE!')

runTest(100)