import socket
import threading
import string
import random
import os
import sys

HOST = os.environ.get("LINK_HOST", "127.0.0.1")
PORT = int(os.environ.get("LINK_PORT", "5000"))

G = "\033[1;32m"
D = "\033[2;32m"
B = "\033[1m"
R = "\033[0m"
DIM = "\033[2m"
BRIGHT = "\033[92m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"

rooms = {}
lock = threading.Lock()


def log(msg):
    print(f"  {G}▸{R} {msg}")


def log_room(code, msg):
    print(f"  {D}[{code}]{R} {msg}")


def warn(msg):
    print(f"  {YELLOW}⚠ {msg}{R}")


def generate_code(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


def broadcast(room_code, message, _client=None):
    with lock:
        for client in list(rooms.get(room_code, {}).get("clients", {}).keys()):
            if client != _client:
                try:
                    client.send(message)
                except (BrokenPipeError, ConnectionResetError, OSError):
                    pass


def handle_client(client):
    username = None
    room_code = None

    try:
        client.send("NICK".encode('utf-8'))
        username = client.recv(1024).decode('utf-8').strip()

        if not username:
            client.send("ERROR:No username provided".encode('utf-8'))
            client.close()
            return

        with lock:
            active_codes = [c for c, r in rooms.items() if r["clients"]]
            if not active_codes:
                client.send("NO_ROOMS".encode('utf-8'))
            else:
                room_list = ",".join(active_codes)
                client.send(f"ROOM_LIST:{room_list}".encode('utf-8'))

            resp = client.recv(1024).decode('utf-8').strip()

            if resp.startswith("CREATE:"):
                room_code = generate_code()
                while room_code in rooms:
                    room_code = generate_code()
                rooms[room_code] = {"clients": {client: username}, "owner": username}
                client.send(f"CREATED:{room_code}".encode('utf-8'))
                log_room(room_code, f"{BRIGHT}{username}{R} created room")

            elif resp.startswith("JOIN:"):
                room_code = resp.split(":", 1)[1].strip().upper()
                if room_code not in rooms:
                    warn(f"{username} tried to join room \"{room_code}\" — not found")
                    client.send("BAD_CODE".encode('utf-8'))
                    client.close()
                    return
                rooms[room_code]["clients"][client] = username
                client.send(f"JOINED:{room_code}".encode('utf-8'))

            elif resp == "JOIN_LATEST":
                if not active_codes:
                    client.send("NO_ROOMS".encode('utf-8'))
                    client.close()
                    return
                room_code = active_codes[-1]
                rooms[room_code]["clients"][client] = username
                client.send(f"JOINED:{room_code}".encode('utf-8'))

            else:
                client.send("ERROR:Invalid response".encode('utf-8'))
                client.close()
                return

        log_room(room_code, f"{BRIGHT}{username}{R} joined")
        broadcast(room_code, f"📢 {username} joined the room!".encode('utf-8'), client)

        if room_code in rooms and rooms[room_code]["clients"]:
            count = len(rooms[room_code]["clients"])
            client.send(f"ROOM_INFO:{room_code}:{count}".encode('utf-8'))

        while True:
            message = client.recv(1024)
            if not message:
                break
            broadcast(room_code, f"{username}: {message.decode('utf-8')}".encode('utf-8'), client)

    except ConnectionResetError:
        warn(f"Connection reset — {username or 'unknown user'} disconnected")
    except BrokenPipeError:
        warn(f"Pipe broken — {username or 'unknown user'} disconnected")
    except OSError as e:
        warn(f"Network error with {username or 'unknown user'}: {e}")
    except Exception as e:
        warn(f"Unexpected error with {username or 'unknown user'}: {e}")

    if room_code and room_code in rooms:
        with lock:
            rooms[room_code]["clients"].pop(client, None)
            log_room(room_code, f"{DIM}{username} left{R}")
            broadcast(room_code, f"📢 {username} left the room.".encode('utf-8'))
            if not rooms[room_code]["clients"]:
                del rooms[room_code]
                log_room(room_code, f"{DIM}room deleted (empty){R}")

    try:
        client.close()
    except OSError:
        pass


def receive_connections():
    print(f"""
{G}      ██╗     ██╗███╗   ██╗██╗  ██╗{R}
{G}      ██║     ██║████╗  ██║██║ ██╔╝{R}
{G}      ██║     ██║██╔██╗ ██║█████╔╝ {R}
{G}      ██║     ██║██║╚██╗██║██╔═██╗ {R}
{G}      ███████╗██║██║ ╚████║██║  ██╗{R}
{G}      ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝{R}
{D}      Live Instant Network Kommunication — server{R}
""")

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
    except OSError as e:
        print(f"  {RED}✗ Can't start server: {e}{R}")
        if "Address already in use" in str(e):
            print(f"  {DIM}  → Port {PORT} is already in use.{R}")
            print(f"  {DIM}  → Kill the other process or use: LINK_PORT=5001 lnk server{R}")
        elif "Permission denied" in str(e):
            print(f"  {DIM}  → Port {PORT} requires admin privileges.{R}")
            print(f"  {DIM}  → Try a higher port: LINK_PORT=8080 lnk server{R}")
        sys.exit(1)

    log(f"{B}Listening{R} on {BRIGHT}{HOST}:{PORT}{R}")
    log(f"{DIM}Waiting for connections...{R}\n")

    while True:
        try:
            client, address = server.accept()
            log(f"{BRIGHT}{address[0]}:{address[1]}{R} connected")
            thread = threading.Thread(target=handle_client, args=(client,), daemon=True)
            thread.start()
        except KeyboardInterrupt:
            print(f"\n\n  {G}👋 Server shutting down.{R}\n")
            server.close()
            sys.exit(0)
        except OSError as e:
            warn(f"Couldn't accept connection: {e}")


if __name__ == "__main__":
    receive_connections()
