import socket
import threading
import sys
import os
import time
import itertools

DEFAULT_HOST = os.environ.get("LINK_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("LINK_PORT", "5000"))


G = "\033[1;32m"
D = "\033[2;32m"
B = "\033[1m"
R = "\033[0m"
W = "\033[1;37m"
DIM = "\033[2m"
BRIGHT = "\033[92m"
RED = "\033[1;31m"


def clear():
    os.system('clear' if os.name == 'posix' else 'cls')


def spinner(msg, duration=1.5):
    chars = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
    end = time.time() + duration
    while time.time() < end:
        sys.stdout.write(f"\r  {G}{next(chars)}{R} {DIM}{msg}{R}")
        sys.stdout.flush()
        time.time()
        time.sleep(0.08)
    sys.stdout.write(f"\r  {G}✓{R} {msg}\n")
    sys.stdout.flush()


def show_banner():
    clear()
    print(f"""
{G}      ██╗     ██╗███╗   ██╗██╗  ██╗{R}
{G}      ██║     ██║████╗  ██║██║ ██╔╝{R}
{G}      ██║     ██║██╔██╗ ██║█████╔╝ {R}
{G}      ██║     ██║██║╚██╗██║██╔═██╗ {R}
{G}      ███████╗██║██║ ╚████║██║  ██╗{R}
{G}      ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝{R}
{D}      Live Instant Network Kommunication{R}
""")


def show_menu():
    print(f"""
{G}  ┌─────────────────────────────────┐{R}
{G}  │{R}  {B}1{R})  Create a new room          {G}│{R}
{G}  │{R}  {B}2{R})  Join by invite code        {G}│{R}
{G}  │{R}  {B}3{R})  Join latest room           {G}│{R}
{G}  │{R}  {B}q{R})  Quit                       {G}│{R}
{G}  └─────────────────────────────────┘{R}
""")


def receive_messages(client, username):
    while True:
        try:
            message = client.recv(4096).decode('utf-8')
            if not message:
                print(f"\n  {RED}× Disconnected from server.{R}")
                client.close()
                break
            if message.startswith("📢"):
                print(f"\r  {DIM}{message}{R}")
            else:
                parts = message.split(":", 1)
                if len(parts) == 2:
                    print(f"\r  {G}▸{R} {B}{parts[0]}{R}: {parts[1]}")
                else:
                    print(f"\r  {message}")
        except:
            print(f"\n  {RED}× Connection lost.{R}")
            client.close()
            break


def send_messages(client, username):
    while True:
        try:
            msg = input(f"  {G}▸{R} ")
            if msg.lower() == 'quit':
                print(f"\n  {G}👋 Goodbye!{R}\n")
                client.close()
                sys.exit(0)
            if msg.strip():
                client.send(msg.encode('utf-8'))
        except:
            break


def show_room_info(code, count):
    print(f"""
{G}  ╔═════════════════════════════════╗{R}
{G}  ║{R}  {B}Room:{R}  {BRIGHT}{code}{R}
{G}  ║{R}  {B}Users:{R} {BRIGHT}{count}{R} online
{G}  ╚═════════════════════════════════╝{R}
""")


def show_invite(code):
    print(f"""
{G}  ╔═════════════════════════════════╗{R}
{G}  ║{R}  {B}Room created!{R}
{G}  ║{R}
{G}  ║{R}  {B}Invite code:{R}  {BRIGHT}{code}{R}
{G}  ║{R}
{G}  ║{R}  {DIM}Share this code with friends{R}
{G}  ║{R}  {DIM}so they can join your room{R}
{G}  ╚═════════════════════════════════╝{R}
""")


def run_client(host=DEFAULT_HOST, port=DEFAULT_PORT):
    show_banner()

    username = input(f"  {G}▸{R} {B}Enter your username:{R} ").strip()
    if not username:
        print(f"  {RED}× Username cannot be empty.{R}")
        return

    spinner("Connecting to server...", 1.2)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except ConnectionRefusedError:
        print(f"\n  {RED}× Could not connect to {host}:{port}{R}")
        print(f"  {DIM}Make sure the server is running:{R} {B}lnk server{R}\n")
        return

    client.send(username.encode('utf-8'))

    response = client.recv(4096).decode('utf-8')

    if response == "NICK":
        client.send(username.encode('utf-8'))
        response = client.recv(4096).decode('utf-8')

    room_code = None
    join_code = os.environ.get("LINK_JOIN_CODE")
    create_room = os.environ.get("LINK_CREATE")

    if join_code:
        spinner(f"Joining room {join_code}...", 0.8)
        client.send(f"JOIN:{join_code}".encode('utf-8'))
        resp = client.recv(4096).decode('utf-8')
        if resp.startswith("JOINED:"):
            room_code = resp.split(":", 1)[1]
            print(f"  {G}✓ Joined room {room_code}!{R}\n")
        elif resp == "BAD_CODE":
            print(f"  {RED}× Invalid invite code: {join_code}{R}")
            client.close()
            return

    elif create_room:
        spinner("Creating room...", 0.8)
        client.send("CREATE:".encode('utf-8'))
        resp = client.recv(4096).decode('utf-8')
        if resp.startswith("CREATED:"):
            room_code = resp.split(":", 1)[1]
            show_invite(room_code)

    elif response.startswith("ROOM_LIST:"):
        codes = response.split(":", 1)[1].split(",") if response.split(":", 1)[1] else []
        print()
        show_menu()

        while True:
            choice = input(f"  {G}▸{R} {B}Choose:{R} ").strip()

            if choice == "1":
                spinner("Creating room...", 0.8)
                client.send("CREATE:".encode('utf-8'))
                resp = client.recv(4096).decode('utf-8')
                if resp.startswith("CREATED:"):
                    room_code = resp.split(":", 1)[1]
                    show_invite(room_code)
                break

            elif choice == "2":
                code = input(f"  {G}▸{R} {B}Enter invite code:{R} ").strip().upper()
                spinner(f"Joining {code}...", 0.8)
                client.send(f"JOIN:{code}".encode('utf-8'))
                resp = client.recv(4096).decode('utf-8')
                if resp.startswith("JOINED:"):
                    room_code = resp.split(":", 1)[1]
                    print(f"  {G}✓ Joined room {room_code}!{R}\n")
                    break
                elif resp == "BAD_CODE":
                    print(f"  {RED}× Invalid code. Try again.{R}")
                    continue

            elif choice == "3":
                spinner("Joining latest room...", 0.8)
                client.send("JOIN_LATEST".encode('utf-8'))
                resp = client.recv(4096).decode('utf-8')
                if resp.startswith("JOINED:"):
                    room_code = resp.split(":", 1)[1]
                    print(f"  {G}✓ Joined room {room_code}!{R}\n")
                    break
                elif resp == "NO_ROOMS":
                    print(f"  {RED}× No active rooms. Create one first.{R}")
                    continue

            elif choice.lower() == 'q':
                print(f"\n  {G}👋 Goodbye!{R}\n")
                client.close()
                return

    elif response == "NO_ROOMS":
        print(f"\n  {DIM}No active rooms.{R}")
        choice = input(f"  {G}▸{R} {B}Create one? (y/n):{R} ").strip().lower()
        if choice == 'y':
            spinner("Creating room...", 0.8)
            client.send("CREATE:".encode('utf-8'))
            resp = client.recv(4096).decode('utf-8')
            if resp.startswith("CREATED:"):
                room_code = resp.split(":", 1)[1]
                show_invite(room_code)
        else:
            client.close()
            return

    info = client.recv(4096).decode('utf-8')
    if info.startswith("ROOM_INFO:"):
        parts = info.split(":")
        code = parts[1]
        count = parts[2]
        show_room_info(code, count)

    print(f"  {DIM}Type messages to chat. Type 'quit' to exit.{R}\n")

    recv_thread = threading.Thread(target=receive_messages, args=(client, username), daemon=True)
    recv_thread.start()

    send_messages(client, username)


if __name__ == "__main__":
    run_client()
