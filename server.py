import socket
import threading
import random
import time
from datetime import datetime
import atexit

HOST = "0.0.0.0"
PORT = 5000

COLORS = [
    "\033[31m", "\033[32m", "\033[33m",
    "\033[34m", "\033[35m", "\033[36m"
]

RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"

SERVER_ASCII = f"""{RED}
  ____  __  _____   ___  __ __   ___________ _   _________ 
 / __ \\/ / / / _ | / _ \\/ //_ /  / __/ __/ _ \\ | / / __/ _ \\
/ /_/ / /_/ / __ |/ , _/ ,<    _\\ \\/ _// , _/ |/ / _// , _/
\\___\\_\\____/_/ |_/_/|_/_/|_|  /___/___/_/|_||___/___/_/|_| 
{RESET}
"""

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = open(f"logs/chat_{timestamp}.log", "a", encoding="utf-8")

def log(msg):
    ts = datetime.now().strftime("[%H:%M:%S]")
    log_file.write(f"{ts} {msg}\n")
    log_file.flush()

@atexit.register
def cleanup():
    log_file.close()

server = socket.socket()
server.bind((HOST, PORT))
server.listen()

clients = {}
usernames = set()
chat_history = []
total_messages = 0
start_time = time.time()

lock = threading.Lock()

print(SERVER_ASCII)
print(f"{GREEN}Server running on {HOST}:{PORT}{RESET}")
log("Server started")

def broadcast(message, exclude=None):
    with lock:
        conns = list(clients.keys())

    for conn in conns:
        if conn != exclude:
            try:
                conn.sendall((message + "\n").encode())
            except:
                conn.close()
                with lock:
                    clients.pop(conn, None)

def send_history(conn):
    conn.sendall(f"{CYAN}--- Chat History ---{RESET}\n".encode())
    for msg in chat_history[-50:]:
        conn.sendall((msg + "\n").encode())
    conn.sendall(f"{CYAN}--- End ---{RESET}\n".encode())

def get_conn_by_username(name):
    with lock:
        for conn, (username, _) in clients.items():
            if username == name:
                return conn
    return None

def handle_client(conn, addr):
    global total_messages

    try:
        username = conn.recv(1024).decode().strip()

        with lock:
            if not username or username in usernames:
                conn.sendall("TAKEN\n".encode())
                conn.close()
                return

            color = random.choice(COLORS)
            usernames.add(username)
            clients[conn] = (username, color)

        conn.sendall("OK\n".encode())
        send_history(conn)

        join_msg = f"{color}[+] {username} joined the chat{RESET}"
        chat_history.append(join_msg)
        broadcast(join_msg)
        log(f"{username} joined")

        while True:
            msg = conn.recv(1024).decode().strip()
            if not msg or msg == "/exit":
                break

            if len(msg) > 300:
                conn.sendall("Message too long (max 300 chars)\n".encode())
                continue

            if msg == "/history":
                send_history(conn)
                continue

            if msg == "/shrug":
                msg = "¯\\_(ツ)_/¯"

            if msg.startswith("/pm "):
                parts = msg.split(" ", 2)
                if len(parts) < 3:
                    conn.sendall("Usage: /pm <user> <message>\n".encode())
                    continue

                target_name = parts[1]
                private_msg = parts[2]

                target_conn = get_conn_by_username(target_name)
                if not target_conn:
                    conn.sendall(f"User '{target_name}' not found.\n".encode())
                    continue

                sender_name, sender_color = clients[conn]

                pm_target = f"{MAGENTA}[PM]{RESET} {sender_color}{sender_name}{RESET}: {private_msg}"
                pm_sender = f"{MAGENTA}[PM → {target_name}]{RESET}: {private_msg}"

                target_conn.sendall((pm_target + "\n").encode())
                conn.sendall((pm_sender + "\n").encode())

                log(f"PM {sender_name} -> {target_name}: {private_msg}")
                continue

            total_messages += 1
            formatted = f"{color}{username}{RESET}: {msg}"
            chat_history.append(formatted)
            broadcast(formatted, exclude=conn)
            log(f"{username}: {msg}")

    except:
        pass
    finally:
        with lock:
            if conn in clients:
                username, _ = clients[conn]
                usernames.discard(username)
                clients.pop(conn, None)

        leave_msg = f"{RED}[-] {username} left the chat{RESET}"
        chat_history.append(leave_msg)
        broadcast(leave_msg)
        log(f"{username} left")
        conn.close()

def accept_clients():
    while True:
        conn, addr = server.accept()
        threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        ).start()

def server_commands():
    while True:
        cmd = input().strip()

        if cmd == "/stats":
            uptime = int(time.time() - start_time)
            print(f"""{YELLOW}
Users online : {len(usernames)}
Total messages: {total_messages}
Uptime        : {uptime}s
{RESET}""")

        elif cmd == "/users":
            print(f"{CYAN}Online users:{RESET}", ", ".join(usernames))

        elif cmd.startswith("/announce "):
            text = cmd[len("/announce "):]
            ann = f"{MAGENTA}[ANNOUNCEMENT]{RESET} {text}"
            chat_history.append(ann)
            broadcast(ann)
            log(f"ANNOUNCEMENT: {text}")

        elif cmd == "/help":
            print("/stats /users /announce <msg> /help")

threading.Thread(target=accept_clients, daemon=True).start()
server_commands()
