import socket
import sys
import os
import subprocess
from distlib.compat import raw_input
from datetime import datetime
from Log import Logs

target_host = "0.0.0.0"  # IP do servidor
target_port = 9999  # Porta de conexão com o servidor
downloadDir = "arquivos"

#Diretorio para verificar se o arquivo existe ou nao
diretorio = os.getcwd()

dataHoje = datetime.today().strftime('%d/%m/%Y')
hora = datetime.today().strftime('%Hh%M')

user = os.path.expanduser('~') #/home/diego
user = user[6:] #Pegando da substr 6 até o final

print("--Arquivos--")
arquivos = os.listdir('/home/diego/tcpSocket/')
for arquivo in arquivos:
    print(arquivo)
    
filename = raw_input("\nDigite o nome do arquivo que quer baixar: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))  # Conecta a um socket remoto passando os parâmetros host, porta
client.send(bytes(filename, 'utf-8')) #converte a string filename para byte e envia para o socket do servidor

#response = client.recv(16384)  # Recebe dados do socket remoto em um determinado tamanho de buffer
#print(str(response, "utf-8"))  # Converte os bytes recebidos em string codificação UTF-8    

#Chamando funcao que verifica se o arquivo existe ou nao
isExist = os.path.exists(diretorio + "/" + filename)


if(isExist):
    with open(os.path.join(downloadDir, filename), 'wb') as file_to_write:
        while True:
            data = client.recv(9999)
            if not data:
                break
            file_to_write.write(data)
            print("Baixando arquivo...")

        file_to_write.close()
        print("Arquivo Baixado com sucesso!")
        client.close()
    #Se o arquivo nao existir    
else:
    print("Arquivo inexistente.")
    print("Erro: " + "FILE_NOT_FOUND")
    log = Logs("Data: " + str(dataHoje) + " - " + "Hora: " + str(hora) + " - " + "IP: " + str(client.getsockname()[0]) + " - " + "Porta: " + str(client.getsockname()[1]) + " - " + "Usuario: " + user + " - " + "Erro: " + "FileNotFoundException")
    client.close()

