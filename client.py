import socket
import threading
import sys
import os
import time
import itertools
import readline

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
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
GRAY = "\033[90m"


def clear():
    os.system('clear' if os.name == 'posix' else 'cls')


def spinner(msg, duration=1.5):
    chars = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
    end = time.time() + duration
    while time.time() < end:
        sys.stdout.write(f"\r  {G}{next(chars)}{R} {DIM}{msg}{R}")
        sys.stdout.flush()
        time.sleep(0.08)
    sys.stdout.write(f"\r  {G}✓{R} {msg}\n")
    sys.stdout.flush()


def error(msg, hint=None):
    print(f"  {RED}✗ {msg}{R}")
    if hint:
        print(f"  {DIM}  → {hint}{R}")


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


def show_chat_header(code, username, count):
    print(f"\n  {CYAN}🔗 L.I.N.K.{R}  {DIM}·{R}  {B}Room {code}{R}  {DIM}·{R}  {count} online{R}")
    print(f"  {DIM}Logged in as {username} · /quit to leave{R}\n")


def receive_messages(client, username):
    while True:
        try:
            message = client.recv(4096).decode('utf-8')
            if not message:
                print(f"\n  {YELLOW}⚠ Server shut down the connection.{R}")
                client.close()
                break
            if message.startswith("📢"):
                print(f"\r  {GRAY}  {message}{R}")
                sys.stdout.write(f"  {G}>{R} ")
                sys.stdout.flush()
            else:
                parts = message.split(":", 1)
                if len(parts) == 2:
                    name = parts[0]
                    text = parts[1]
                    print(f"\r  {BRIGHT}{name}{R}  {DIM}▸{R}  {text}")
                    sys.stdout.write(f"  {G}>{R} ")
                    sys.stdout.flush()
                else:
                    print(f"\r  {message}")
                    sys.stdout.write(f"  {G}>{R} ")
                    sys.stdout.flush()
        except ConnectionResetError:
            print(f"\n  {YELLOW}⚠ Server closed the connection unexpectedly.{R}")
            print(f"  {DIM}  → The server may have restarted.{R}")
            client.close()
            break
        except OSError:
            client.close()
            break
        except Exception as e:
            print(f"\n  {RED}✗ Lost connection: {e}{R}")
            client.close()
            break


def send_messages(client, username):
    while True:
        try:
            msg = input(f"  {G}>{R} ")
            if msg.lower() in ('/quit', 'quit', '/exit', '/q'):
                print(f"\n  {G}👋 Goodbye!{R}\n")
                client.send(f"{username} left the chat.".encode('utf-8'))
                client.close()
                sys.exit(0)
            if msg.strip():
                client.send(msg.encode('utf-8'))
        except BrokenPipeError:
            print(f"\n  {RED}✗ Can't send — not connected to server.{R}")
            print(f"  {DIM}  → The server may have stopped.{R}")
            break
        except ConnectionResetError:
            print(f"\n  {RED}✗ Connection was reset by the server.{R}")
            break
        except OSError:
            break
        except KeyboardInterrupt:
            print(f"\n\n  {G}👋 Goodbye!{R}\n")
            client.close()
            sys.exit(0)


def show_room_info(code, count):
    print(f"""
{G}  ╔═════════════════════════════════╗{R}
{G}  ║{R}  {B}Room:{R}  {BRIGHT}{code}{R}
{G}  ║{R}  {B}Users:{R} {BRIGHT}{count}{R} online
{G}  ╚═════════════════════════════════╝{R}
""")


def show_invite(code):
    print(f"\n  {G}🔗 Room created!{R}")
    print(f"  {B}Code:{R} {BRIGHT}{code}{R}")
    print(f"  {DIM}lnk join {code}{R}\n")


def run_client(host=DEFAULT_HOST, port=DEFAULT_PORT):
    show_banner()

    username = input(f"  {G}>{R} {B}Enter your username:{R} ").strip()
    if not username:
        error("Username can't be empty.", "Type a name and press Enter.")
        return
    if len(username) > 20:
        error("Username is too long (max 20 characters).", "Pick a shorter name.")
        return

    spinner("Connecting to server...", 1.2)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except ConnectionRefusedError:
        error(f"Can't connect to {host}:{port}", "Is the server running? Try: lnk server")
        return
    except TimeoutError:
        error(f"Connection timed out to {host}:{port}", "Check your network and try again.")
        return
    except OSError as e:
        error(f"Network error: {e}", "Check your internet connection.")
        return

    try:
        response = client.recv(4096).decode('utf-8')
    except ConnectionResetError:
        error("Server dropped the connection.", "Try running: lnk server")
        return
    except OSError as e:
        error(f"Connection error: {e}", "Check your network connection.")
        return

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
            print(f"  {G}✓ Joined room {room_code}!{R}")
        elif resp == "BAD_CODE":
            error(f"No room found with code \"{join_code}\".", "Check the code and try again. Room codes are 6 characters (e.g. A7X3KP).")
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
            choice = input(f"  {G}>{R} {B}Choose:{R} ").strip()

            if choice == "1":
                spinner("Creating room...", 0.8)
                client.send("CREATE:".encode('utf-8'))
                resp = client.recv(4096).decode('utf-8')
                if resp.startswith("CREATED:"):
                    room_code = resp.split(":", 1)[1]
                    show_invite(room_code)
                break

            elif choice == "2":
                code = input(f"  {G}>{R} {B}Enter invite code:{R} ").strip().upper()
                if not code:
                    error("Invite code can't be empty.", "Paste or type the 6-character code.")
                    continue
                spinner(f"Joining {code}...", 0.8)
                client.send(f"JOIN:{code}".encode('utf-8'))
                resp = client.recv(4096).decode('utf-8')
                if resp.startswith("JOINED:"):
                    room_code = resp.split(":", 1)[1]
                    print(f"  {G}✓ Joined room {room_code}!{R}")
                    break
                elif resp == "BAD_CODE":
                    error(f"No room found with code \"{code}\".", "Double-check the code. It's 6 characters like A7X3KP.")
                    continue

            elif choice == "3":
                spinner("Joining latest room...", 0.8)
                client.send("JOIN_LATEST".encode('utf-8'))
                resp = client.recv(4096).decode('utf-8')
                if resp.startswith("JOINED:"):
                    room_code = resp.split(":", 1)[1]
                    print(f"  {G}✓ Joined room {room_code}!{R}")
                    break
                elif resp == "NO_ROOMS":
                    error("No rooms exist yet.", "Create one first with option 1.")
                    continue

            elif choice.lower() == 'q':
                print(f"\n  {G}👋 Goodbye!{R}\n")
                client.close()
                return

            else:
                error("Invalid option.", "Pick 1, 2, 3, or q.")

    elif response == "NO_ROOMS":
        print(f"\n  {DIM}No rooms exist yet.{R}")
        choice = input(f"  {G}>{R} {B}Create one? (y/n):{R} ").strip().lower()
        if choice in ('y', 'yes'):
            spinner("Creating room...", 0.8)
            client.send("CREATE:".encode('utf-8'))
            resp = client.recv(4096).decode('utf-8')
            if resp.startswith("CREATED:"):
                room_code = resp.split(":", 1)[1]
                show_invite(room_code)
        else:
            client.close()
            return

    try:
        info = client.recv(4096).decode('utf-8')
        if info.startswith("ROOM_INFO:"):
            parts = info.split(":")
            code = parts[1]
            count = parts[2]
            show_chat_header(code, username, count)
    except (ConnectionResetError, OSError):
        pass

    recv_thread = threading.Thread(target=receive_messages, args=(client, username), daemon=True)
    recv_thread.start()

    send_messages(client, username)


if __name__ == "__main__":
    run_client()
