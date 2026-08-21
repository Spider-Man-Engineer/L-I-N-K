import socket
import threading
import sys
import os
import time
import itertools
import readline
import hashlib
import random

DEFAULT_HOST = os.environ.get("LINK_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("LINK_PORT", "5000"))

R = "\033[0m"
B = "\033[1m"
DIM = "\033[2m"
RED = "\033[1;31m"
GRAY = "\033[90m"

THEMES = {
    "green":    {"p": "\033[1;32m", "d": "\033[2;32m", "b": "\033[92m"},
    "pink":     {"p": "\033[1;35m", "d": "\033[2;35m", "b": "\033[95m"},
    "blue":     {"p": "\033[1;34m", "d": "\033[2;34m", "b": "\033[94m"},
    "cyan":     {"p": "\033[1;36m", "d": "\033[2;36m", "b": "\033[96m"},
    "yellow":   {"p": "\033[1;33m", "d": "\033[2;33m", "b": "\033[93m"},
    "red":      {"p": "\033[1;31m", "d": "\033[2;31m", "b": "\033[91m"},
    "magenta":  {"p": "\033[35m",   "d": "\033[2;35m", "b": "\033[95m"},
    "white":    {"p": "\033[1;37m", "d": "\033[2;37m", "b": "\033[97m"},
}

USER_COLORS = [
    "\033[1;31m", "\033[1;32m", "\033[1;33m", "\033[1;34m",
    "\033[1;35m", "\033[1;36m", "\033[91m", "\033[93m",
    "\033[94m", "\033[95m", "\033[96m", "\033[97m",
]


def user_color(username):
    h = int(hashlib.md5(username.encode()).hexdigest(), 16)
    return USER_COLORS[h % len(USER_COLORS)]


def get_theme(username):
    h = int(hashlib.md5(username.encode()).hexdigest(), 16)
    names = list(THEMES.keys())
    name = names[h % len(names)]
    return THEMES[name], name


def clear():
    os.system('clear' if os.name == 'posix' else 'cls')


def spinner(theme, msg, duration=1.2):
    p = theme["p"]
    chars = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
    end = time.time() + duration
    while time.time() < end:
        sys.stdout.write(f"\r  {p}{next(chars)}{R} {DIM}{msg}{R}")
        sys.stdout.flush()
        time.sleep(0.08)
    sys.stdout.write(f"\r  {p}✓{R} {msg}\n")
    sys.stdout.flush()


def error(msg, hint=None):
    print(f"  {RED}✗ {msg}{R}")
    if hint:
        print(f"  {DIM}  → {hint}{R}")


def show_banner(theme):
    p = theme["p"]
    d = theme["d"]
    print(f"""
{p}      ██╗     ██╗███╗   ██╗██╗  ██╗{R}
{p}      ██║     ██║████╗  ██║██║ ██╔╝{R}
{p}      ██║     ██║██╔██╗ ██║█████╔╝ {R}
{p}      ██║     ██║██║╚██╗██║██╔═██╗ {R}
{p}      ███████╗██║██║ ╚████║██║  ██╗{R}
{p}      ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝{R}
{d}      Live Instant Network Kommunication{R}
""")


def show_menu(theme):
    p = theme["p"]
    print(f"""
{p}  ┌─────────────────────────────────┐{R}
{p}  │{R}  {B}1{R})  Create a new room          {p}│{R}
{p}  │{R}  {B}2{R})  Join by invite code        {p}│{R}
{p}  │{R}  {B}3{R})  Join latest room           {p}│{R}
{p}  │{R}  {B}q{R})  Quit                       {p}│{R}
{p}  └─────────────────────────────────┘{R}
""")


def show_chat_header(theme, code, username, count):
    p = theme["p"]
    c = user_color(username)
    print(f"\n  {p}✓{R} Room {B}{code}{R} · {count} online")
    print(f"  {DIM}{c}{username}{R} {DIM}· /quit to leave{R}\n")


def show_invite(theme, code):
    p = theme["p"]
    d = theme["d"]
    print(f"\n  {p}✓ Room created{R}")
    print(f"  {B}{code}{R}")
    print(f"  {d}lnk join {code}{R}\n")


def receive_messages(theme, client, username):
    p = theme["p"]
    while True:
        try:
            message = client.recv(4096).decode('utf-8')
            if not message:
                print(f"\n  {RED}⚠ Server shut down.{R}")
                client.close()
                break
            if message.startswith("📢"):
                print(f"\r  {GRAY}  {message}{R}")
                print()
                sys.stdout.write(f"  {p}›{R} ")
                sys.stdout.flush()
            else:
                parts = message.split(":", 1)
                if len(parts) == 2:
                    name = parts[0]
                    text = parts[1]
                    c = user_color(name)
                    print(f"\r\n  {c}{name}{R}  {DIM}›{R}  {text}\n")
                    sys.stdout.write(f"  {p}›{R} ")
                    sys.stdout.flush()
                else:
                    print(f"\r  {message}")
                    sys.stdout.write(f"  {p}›{R} ")
                    sys.stdout.flush()
        except ConnectionResetError:
            print(f"\n  {RED}⚠ Server closed.{R}")
            client.close()
            break
        except OSError:
            client.close()
            break
        except Exception as e:
            print(f"\n  {RED}✗ Lost connection.{R}")
            client.close()
            break


def send_messages(theme, client, username):
    p = theme["p"]
    while True:
        try:
            msg = input(f"  {p}›{R} ")
            if msg.lower() in ('/quit', 'quit', '/exit', '/q'):
                print(f"\n  {p}👋 Goodbye!{R}\n")
                client.send(f"{username} left the chat.".encode('utf-8'))
                client.close()
                sys.exit(0)
            if msg.strip():
                client.send(msg.encode('utf-8'))
        except BrokenPipeError:
            print(f"\n  {RED}✗ Can't send — not connected to server.{R}")
            break
        except ConnectionResetError:
            print(f"\n  {RED}✗ Connection was reset by the server.{R}")
            break
        except OSError:
            break
        except KeyboardInterrupt:
            print(f"\n\n  {p}👋 Goodbye!{R}\n")
            client.close()
            sys.exit(0)


def boot(theme):
    p = theme["p"]
    print(f"\n  {DIM}Initializing...{R}\n")
    time.sleep(0.3)
    print(f"  {p}✓{R} Network loaded")
    time.sleep(0.2)
    print(f"  {p}✓{R} Identity loaded")
    time.sleep(0.2)
    print(f"  {p}✓{R} Ready\n")


def run_client(host=DEFAULT_HOST, port=DEFAULT_PORT):
    clear()

    print(f"  {DIM}Enter a username to get started{R}\n")
    username = input(f"  {B}›{R} ").strip()
    if not username:
        error("Username can't be empty.", "Type a name and press Enter.")
        return
    if len(username) > 20:
        error("Username is too long (max 20 characters).", "Pick a shorter name.")
        return

    theme, theme_name = get_theme(username)
    p = theme["p"]

    clear()
    show_banner(theme)
    boot(theme)

    print(f"  {p}✓{R} {B}{username}{R} {DIM}({theme_name}){R}\n")

    spinner(theme, "Connecting to LINK network...", 1.2)

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

    print(f"  {p}✓{R} Connected")

    room_code = None
    join_code = os.environ.get("LINK_JOIN_CODE")
    create_room = os.environ.get("LINK_CREATE")

    if join_code:
        spinner(theme, f"Joining room {join_code}...", 0.8)
        client.send(f"JOIN:{join_code}".encode('utf-8'))
        resp = client.recv(4096).decode('utf-8')
        if resp.startswith("JOINED:"):
            room_code = resp.split(":", 1)[1]
            print(f"  {p}✓{R} Joined {B}{room_code}{R}")
        elif resp == "BAD_CODE":
            error(f"No room found with code \"{join_code}\".", "Check the code. It's 6 characters like A7X3KP.")
            client.close()
            return

    elif create_room:
        spinner(theme, "Creating room...", 0.8)
        client.send("CREATE:".encode('utf-8'))
        resp = client.recv(4096).decode('utf-8')
        if resp.startswith("CREATED:"):
            room_code = resp.split(":", 1)[1]
            show_invite(theme, room_code)

    elif response.startswith("ROOM_LIST:"):
        codes = response.split(":", 1)[1].split(",") if response.split(":", 1)[1] else []
        show_menu(theme)

        while True:
            choice = input(f"  {p}›{R} {B}Choose:{R} ").strip()

            if choice == "1":
                spinner(theme, "Creating room...", 0.8)
                client.send("CREATE:".encode('utf-8'))
                resp = client.recv(4096).decode('utf-8')
                if resp.startswith("CREATED:"):
                    room_code = resp.split(":", 1)[1]
                    show_invite(theme, room_code)
                break

            elif choice == "2":
                code = input(f"  {p}›{R} {B}Enter invite code:{R} ").strip().upper()
                if not code:
                    error("Invite code can't be empty.", "Type the 6-character code.")
                    continue
                spinner(theme, f"Joining {code}...", 0.8)
                client.send(f"JOIN:{code}".encode('utf-8'))
                resp = client.recv(4096).decode('utf-8')
                if resp.startswith("JOINED:"):
                    room_code = resp.split(":", 1)[1]
                    print(f"  {p}✓{R} Joined {B}{room_code}{R}")
                    break
                elif resp == "BAD_CODE":
                    error(f"No room found with code \"{code}\".", "Double-check the code. It's 6 characters like A7X3KP.")
                    continue

            elif choice == "3":
                spinner(theme, "Joining latest room...", 0.8)
                client.send("JOIN_LATEST".encode('utf-8'))
                resp = client.recv(4096).decode('utf-8')
                if resp.startswith("JOINED:"):
                    room_code = resp.split(":", 1)[1]
                    print(f"  {p}✓{R} Joined {B}{room_code}{R}")
                    break
                elif resp == "NO_ROOMS":
                    error("No rooms exist yet.", "Create one first with option 1.")
                    continue

            elif choice.lower() == 'q':
                print(f"\n  {p}👋 Goodbye!{R}\n")
                client.close()
                return

            else:
                error("Invalid option.", "Pick 1, 2, 3, or q.")

    elif response == "NO_ROOMS":
        print(f"\n  {DIM}No rooms exist yet.{R}")
        choice = input(f"  {p}›{R} {B}Create one? (y/n):{R} ").strip().lower()
        if choice in ('y', 'yes'):
            spinner(theme, "Creating room...", 0.8)
            client.send("CREATE:".encode('utf-8'))
            resp = client.recv(4096).decode('utf-8')
            if resp.startswith("CREATED:"):
                room_code = resp.split(":", 1)[1]
                show_invite(theme, room_code)
        else:
            client.close()
            return

    try:
        info = client.recv(4096).decode('utf-8')
        if info.startswith("ROOM_INFO:"):
            parts = info.split(":")
            code = parts[1]
            count = parts[2]
            show_chat_header(theme, code, username, count)
    except (ConnectionResetError, OSError):
        pass

    recv_thread = threading.Thread(target=receive_messages, args=(theme, client, username), daemon=True)
    recv_thread.start()

    send_messages(theme, client, username)


if __name__ == "__main__":
    run_client()
