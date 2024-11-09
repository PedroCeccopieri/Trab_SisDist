from threading import Thread
import socket as st

sock1Ip, sock1Port = 'localhost', 5555

servers = []

with open('servers.txt', 'r') as f:
    for i in f:
        servers.append(i[:-1].split(', '))

print("## REVERSED PROXY ##")

def socket1():

    print("-- socket 1 created! --\n", end = '')
    sock = st.socket(st.AF_INET, st.SOCK_STREAM)
    sock.bind((sock1Ip, sock1Port))
    sock.listen(100)

    while (True):
        print("-- socket 1 waiting conections --\n", end = '')

        client, address = sock.accept()
        print(f"-- socket 1 has conected with {address} --\n", end = '')
        data = client.recv(1024)
        print(f"-- socket 1 has received a message --\n", end = '')
        print(f"-- socket 1 is calculating --\n", end = '')

        cpuLoad = [getCPU(s[0], int(s[2])) for s in servers]
        choice = cpuLoad.index(min(cpuLoad))

        t = Thread(target = calcThread, args= (client, servers[choice], data))
        t.start()

def calcThread(client, server, data):

    res = send2server(server[0], int(server[1]), data)
    print("-- reverse proxy responding --")
    client.send(str(res).encode("UTF-8"))
    client.close()


def getCPU(ip, port):

    sock = st.socket(st.AF_INET, st.SOCK_STREAM)
    sock.connect((ip, port))

    try: 
        sock.send('cpu'.encode('utf-8'))        
        data = sock.recv(1024)
        data = float(data.decode("UTF-8"))

    except st.error as e:
        print ("Socket error: %s" %str(e))
        data = None

    except Exception as e:
        print ("Other exception: %s" %str(e))
        data = None

    sock.close()
    return data

def send2server(ip, port, msg):

    sock = st.socket(st.AF_INET, st.SOCK_STREAM)
    sock.connect((ip, port))

    try:
        sock.send(msg)       
        data = sock.recv(1024)
        data = float(data.decode("UTF-8"))

    except st.error as e:
        print ("Socket error: %s" %str(e))
        data = None

    except Exception as e:
        print ("Other exception: %s" %str(e))
        data = None

    sock.close()
    return data


def run():
    thread1 = Thread(target = socket1)
    thread1.start()
    # thread2 = Thread(target = socket2)
    # thread2.start()

    thread1.join()
    # thread2.join()
    print ("thread finished...exiting")

run()