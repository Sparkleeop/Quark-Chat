import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 5000

CYAN = "\033[36m"
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

ASCII = f"""{GREEN}
  ____  __  _____   ___  __ __   _______   _________  ________
 / __ \\/ / / / _ | / _ \\/ //_/_  / ___/ /  /  _/ __/ |/ /_  __/
 / /_/ / /_/ / __ |/ , _/ ,<    / /__/ /___/ // _//    / / /   
 \\___\\_\\____/_/ |_/_/|_/_/|_|   \\___/____/___/___/_/|_/ /_/    
{RESET}
"""

print(ASCII)

client = socket.socket()

try:
    client.connect((HOST, PORT))
except:
    print(f"{RED}Server offline or unreachable.{RESET}")
    sys.exit()

username = input("Enter a username: ")
client.sendall((username + "\n").encode())

response = client.recv(1024).decode().strip()
if response == "TAKEN":
    print(f"{RED}Username already taken.{RESET}")
    client.close()
    sys.exit()

print(f"{CYAN}Connected! /history /pm /exit{RESET}")

def receive():
    buffer = ""
    while True:
        try:
            data = client.recv(1024).decode()
            if not data:
                break

            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                print(line)

        except:
            break

threading.Thread(target=receive, daemon=True).start()

while True:
    try:
        msg = input()
        if msg == "/exit":
            client.sendall("/exit\n".encode())
            break
        client.sendall((msg + "\n").encode())
    except:
        break

client.close()
