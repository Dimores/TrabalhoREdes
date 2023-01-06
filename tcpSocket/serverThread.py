import subprocess
import socket
import os
import threading
import sys
from datetime import datetime
from Log import Logs

HOST = '0.0.0.0' #Aceita conexao de qualquer IP
PORT = 9999

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, PORT))
socket.listen(10)
print("Servidor rodando em: " + HOST + ":" + str(PORT))

#Usuário
#user = os.path.expanduser('~') 
#user = user[6:] #Pegando da substr 6 até o final
#print(user)


def getUsuario(conn):
    user = conn.recv(9999)
    user = str(user, "utf-8")
    #print(user)
    return user

def fileSend():
    dataHoje = datetime.today().strftime('%d/%m/%Y')
    hora = datetime.today().strftime('%Hh%M')
    while 1:
        conn, addr = socket.accept()
        print("[*] Conexao aceita de: ", addr[0], ":", addr[1])
        user = getUsuario(conn)
        result = subprocess.run("ls", stdout = subprocess.PIPE)
        conn.send(result.stdout)  # Envia conjunto de bytes (mensagens) para o socket remoto
        reqFile = conn.recv(9999)
        try:
            with open(reqFile, 'rb') as file_to_send:
                for data in file_to_send:
                    conn.sendall(data)
                log = Logs("Data: " + str(dataHoje) + " - " + "Hora: " + str(hora) + " - " + "IP: " + str(addr[0]) + " - " + "Porta: " + str(addr[1]) + " - " + "Usuario: " + user + " - " + "Baixou: " + str(reqFile))
                log.saveLog()
            conn.close()
        except:
            print("Houve um erro")
            log = Logs("Data: " + str(dataHoje) + " - " + "Hora: " + str(hora) + " - " + "IP: " + str(addr[0]) + " - " + "Porta: " + str(addr[1]) + " - " + "Usuario: " + user + " - " + "Erro: " + str(sys.exc_info()[0]))
            log.saveLog()
            conn.close()

    socket.close()
while True:
    client_handler = threading.Thread(target=fileSend())
    client_handler.start()  # Inicia a thread
    
