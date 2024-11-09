from threading import Thread
import socket as st
import psutil
import time

import calculadora

def createServer(id, sock1Ip, sock1Port, sock2Ip, sock2Port):

    thread1 = Thread(target = socket1, args= (id, sock1Ip, sock1Port))
    thread1.start()
    thread2 = Thread(target = socket2, args= (id, sock2Ip, sock2Port))
    thread2.start()

    thread1.join()
    thread2.join()
    print ("thread finished...exiting")

def socket1(serverId, sockIp, sockPort):

    print(f"## SERVER {serverId} ## -- socket 1 created! --\n", end = '')
    sock = st.socket(st.AF_INET, st.SOCK_STREAM)
    sock.bind((sockIp, sockPort))
    sock.listen(100)

    while (True):
        print(f"## SERVER {serverId} ## -- socket 1 waiting conections --\n", end = '')

        client, address = sock.accept()
        print(f"## SERVER {serverId} ## -- socket 1 has conected with {address} --\n", end = '')
        data = client.recv(1024).decode("UTF-8")
        print(f"## SERVER {serverId} ## -- socket 1 has received a message --\n", end = '')

        print(f"\n## SERVER {serverId} ## -- socket 1 is CALCULATING --\n", end = '')
        
        with open("log.txt", "a") as log:
            # log.write(f"## SERVER {serverId} is CALCULATING ##\n")
            log.write(f"{serverId}\n")

        command = data.split(' ')

        # time.sleep(0.01)

        match command[0]:

            case "som":
                res = calculadora.som(int(command[1]), int(command[2]))
                client.send(f"{res}".encode("UTF-8"))
            
            case "sub":
                res = calculadora.sub(int(command[1]), int(command[2]))
                client.send(f"{res}".encode("UTF-8"))

            case "mul":
                res = calculadora.mul(int(command[1]), int(command[2]))
                client.send(f"{res}".encode("UTF-8"))
            
            case "div":
                res = calculadora.div(int(command[1]), int(command[2]))
                client.send(f"{res}".encode("UTF-8"))

        client.close()

def socket2(serverId, sockIp, sockPort):
    print(f"## SERVER {serverId} ## -- socket 2 created! --\n", end = '')
    sock = st.socket(st.AF_INET, st.SOCK_STREAM)
    sock.bind((sockIp, sockPort))
    sock.listen(100)

    while (True):
        print(f"## SERVER {serverId} ## -- socket 2 waiting conections --\n", end = '')
    
        client, address = sock.accept()
        print(f"## SERVER {serverId} ## -- socket 2 has conected with {address} --\n", end = '')
        data = client.recv(1024).decode("UTF-8")
        print(f"## SERVER {serverId} ## -- socket 2 has received a message --\n", end = '')

        print(f"\n## SERVER {serverId} ## -- socket 2 sent the CPU load --\n", end = '')

        if (data == 'cpu'):
            client.send(f'{psutil.cpu_percent()}'.encode("UTF-8"))

        client.close()

servers = []

with open('servers.txt', 'r') as f:
    for i in f:
        servers.append(i[:-1].split(', '))

threads = []

for idx, s in enumerate(servers, 1):
    t = Thread(target=createServer, args= (idx, s[0], int(s[1]), s[0], int(s[2])))
    t.start()
    threads.append(t)

for i in threads:
    i.join()