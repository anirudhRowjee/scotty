# roadmap 1 - send file to fixed client
import socket
import sys
import tkinter as tk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from rich.console import Console
from rich.progress import track
from time import sleep
import re
import json
import pickle
import rich
from simple_term_menu import TerminalMenu

LOGO = '''
                    __  __       
   ______________  / /_/ /___  __
  / ___/ ___/ __ \/ __/ __/ / / /
 (__  ) /__/ /_/ / /_/ /_/ /_/ / 
/____/\___/\____/\__/\__/\__, /  
                        /____/  
'''
BATCH_SIZE = 1024
chosen_port = 0

def action_menu():
    OPTIONS = ["send", "receive", "exit"]
    action_menu = TerminalMenu(OPTIONS)
    return(OPTIONS[action_menu.show()])

def generate_manifest_from_file(filepath):
    # filepath doesn't need to be validated as it is selected from the
    # filepicker object in Tkinter
    size = Path(filepath).stat().st_size
    filename, extension = filepath.split('/')[-1].split('.')
    print(size, filepath, extension)
    manifest = {
        'size': size,
        'filename': filename,
        'extension': extension,
    }
    return manifest


def sendFile():
    console.print("Initializing Socket... ", style='bold red')

    RECIEVER = 'localhost'

    mainsocket = socket.socket()
    mainsocket.bind(("localhost", chosen_port))

    console.print("Completed! Sender Setup at localhost:",chosen_port, style='bold yellow')

    # file chooser
    tk.Tk().withdraw()
    filepath = askopenfilename()

    target_ipv4 = input("Enter Target IP Address on LAN >>> ")

    if validate_ipv4(target_ipv4):
        # target IP is valid
        console.print("IP Is valid! Attempting to Connect to Client...",
                        style = 'bold green'
                      )

        target_port = int(input("Enter Target IP Address's Port >>> "))

        # ping client with socket
        try:

            mainsocket.connect((target_ipv4, target_port))

            '''
            Now that the sockets have established a connection, send the
            manifest - a JSON object that has the file size, file name, and
            extension. This is effectively a handshake process - to allow both
            server and the client to be consenting to a file transfer
            '''

            manifest = generate_manifest_from_file(filepath)
            console.print("sending manifest", style='yellow')
            filesize = manifest['size']

            dump = pickle.dumps(manifest)

            mainsocket.sendall(dump)

            # listen for manifest consent
            answer = pickle.loads(mainsocket.recv(1024))

            if int(answer['answer']) == 1:
                # file sending has been accepted
                console.print("sending file at .. ", filepath, style='bold yellow')

                with open(filepath, 'rb') as file:
                    for step in track(range(0, filesize, BATCH_SIZE)):
                        burst = file.read(BATCH_SIZE)
                        mainsocket.send(burst)

                console.print("File Successfully sent!", style='bold green')

                token = pickle.loads(mainsocket.recv(512))

                if token == 'COMPLETE':
                    console.print("File Successfully Recieved!", style='bold green')
                else:
                    console.print("Some Error", style='bold red')

            else:
                console.print("File Send Request Denied. ", style='bold red')

            mainsocket.close()

        except socket.error:
            console.print("Socket Error! ", error , style='bold red')


    else:
        print("Fail")
        mainsocket.close()



def validate_ipv4(ipv4):
    # :param ipv4 string
    target_regexp = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ipv4)
    if target_regexp:
        return True
    else:
        return False

def recFile():
    # receive file from socket
    console.print("Initializing Socket... ", style='bold red')


    mainsocket = socket.socket()
    mainsocket.bind(("localhost", chosen_port))
    mainsocket.listen(5)

    console.print("Completed! Reciever Setup at localhost:", chosen_port, style='bold yellow')

    target_ipv4 = input("Enter Target IP Address on LAN >>> ")

    if validate_ipv4(target_ipv4):
        # target IP is valid
        console.print("IP Is valid! Attempting to Connect to Client...",
                        style = 'bold green'
                      )

        target_port = int(input("Enter Target IP Address's Port >>> "))

        # ping client with socket
        try:
            console.print("Awaiting server connection...")
            c, addr = mainsocket.accept()
            print("Accepted Connection from {}".format(addr))
            manifest = c.recv(2046)
            manifest = pickle.loads(manifest)


            console.print("{addr} wants to send {name}.{extension} ({size} bytes) ; accept?[y/n]"
                          .format(addr = addr, name=manifest['filename'], extension
                                  = manifest['extension'], size =
                                  manifest['size']),
                          style = 'bold yellow'
                          )

            answer = input(">>> ").lower()

            if answer == 'y':

                # accept and send success signal
                c.send(pickle.dumps({'answer': '1'}))

                filename = "{}.{}".format(manifest['filename'],
                                          manifest['extension'])
                filesize_bytes = int(manifest['size'])

                console.print("Preparing to recieve file ", filename,
                              style='yellow')

                print(" Preparing to recieve file ")

                with open(filename, 'wb') as file:
                    for step in track(range(0, filesize_bytes, BATCH_SIZE)):
                        burst  = c.recv(BATCH_SIZE)
                        file.write(burst)

                console.print("Done! Closing connections...", style='bold green')

                c.send(pickle.dumps("COMPLETE"))

                c.close()

            elif answer == 'n':
                # send failure signal
                c.send(pickle.dumps({'answer': '0'}))
                console.print("Closing Socket Connection...", style='bold red')
                c.close()
            mainsocket.close()

        except socket.error:
            console.print("Socket Error! ", error,  style='bold red')

        mainsocket.close()

    else:
        print("Fail")



if __name__ == '__main__':
    # driver code
    console = rich.console.Console()
    console.print(LOGO, style='bold blue')
    CLIENT = 'localhost'
    chosen_port = int(input("Enter Port to setup Scotty on >>> "))
    console.print("What Do You Want to Do?", style='bold underline green')
    option = action_menu()

    if option == 'send':
        sendFile()

    elif option == 'receive':
        recFile()


