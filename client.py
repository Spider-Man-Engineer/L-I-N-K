import socket
import threading
import sys
import os
import time
import itertools
import readline

DEFAULT_HOST = os.environ.get("LINK_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("LINK_PORT", "5000"))

R = "\033[0m"
B = "\033[1m"
DIM = "\033[2m"
RED = "\033[1;31m"
GRAY = "\033[90m"

THEMES = {
    "green":    {"p": "\033[1;32m", "d": "\033[2;32m"},
    "pink":     {"p": "\033[1;35m", "d": "\033[2;35m"},
    "blue":     {"p": "\033[1;34m", "d": "\033[2;34m"},
    "cyan":     {"p": "\033[1;36m", "d": "\033[2;36m"},
    "yellow":   {"p": "\033[1;33m", "d": "\033[2;33m"},
    "red":      {"p": "\033[1;31m", "d": "\033[2;31m"},
    "magenta":  {"p": "\033[35m",   "d": "\033[2;35m"},
    "white":    {"p": "\033[1;37m", "d": "\033[2;37m"},
}

COLOR_CODES = {
    "red":         "\033[1;31m",
    "green":       "\033[1;32m",
    "yellow":      "\033[1;33m",
    "blue":        "\033[1;34m",
    "magenta":     "\033[1;35m",
    "cyan":        "\033[1;36m",
    "light_red":   "\033[91m",
    "light_green": "\033[92m",
    "light_yellow":"\033[93m",
    "light_blue":  "\033[94m",
    "light_magenta":"\033[95m",
    "light_cyan":  "\033[96m",
    "white":       "\033[97m",
    "orange":      "\033[38;5;208m",
    "purple":      "\033[38;5;129m",
    "pink":        "\033[38;5;213m",
    "lime":        "\033[38;5;118m",
    "teal":        "\033[38;5;30m",
    "coral":       "\033[38;5;204m",
    "gold":        "\033[38;5;220m",
}

user_colors = {}


def get_color(name):
    if name in user_colors:
        return user_colors[name]
    return "\033[1;37m"


def get_theme(username):
    h = hash(username) % len(list(THEMES.keys()))
    name = list(THEMES.keys())[h]
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
    c = get_color(username)
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

            if message.startswith("COLOR:"):
                parts = message.split(":", 2)
                if len(parts) == 3:
                    name = parts[1]
                    color_name = parts[2]
                    if color_name in COLOR_CODES:
                        user_colors[name] = COLOR_CODES[color_name]

            elif message.startswith("JOIN:"):
                name = message.split(":", 1)[1]
                print(f"\n  {GRAY}  {name} joined the room{R}\n")
                sys.stdout.write(f"  {p}›{R} ")
                sys.stdout.flush()

            elif message.startswith("LEFT:"):
                name = message.split(":", 1)[1]
                print(f"\n  {GRAY}  {name} left the room{R}\n")
                sys.stdout.write(f"  {p}›{R} ")
                sys.stdout.flush()

            elif ":" in message:
                name, text = message.split(":", 1)
                c = get_color(name)
                print(f"\n  {c}{name}{R}  {DIM}▸{R}  {text}\n")
                sys.stdout.write(f"  {p}›{R} ")
                sys.stdout.flush()

        except ConnectionResetError:
            print(f"\n  {RED}⚠ Server closed.{R}")
            client.close()
            break
        except OSError:
            client.close()
            break
        except Exception:
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
                client.close()
                sys.exit(0)
            if msg.strip():
                client.send(msg.encode('utf-8'))
        except (BrokenPipeError, ConnectionResetError, OSError):
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
        error("Username can't be empty.")
        return
    if len(username) > 20:
        error("Username too long (max 20).")
        return

    theme, theme_name = get_theme(username)
    p = theme["p"]

    clear()
    show_banner(theme)
    boot(theme)

    print(f"  {p}✓{R} {B}{username}{R} {DIM}({theme_name}){R}\n")

    spinner(theme, "Connecting...", 1.2)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except ConnectionRefusedError:
        error(f"Can't connect to {host}:{port}", "Is the server running? Try: lnk server")
        return
    except TimeoutError:
        error("Connection timed out.")
        return
    except OSError as e:
        error(f"Network error: {e}")
        return

    try:
        response = client.recv(4096).decode('utf-8')
    except (ConnectionResetError, OSError):
        error("Server dropped connection.", "Try: lnk server")
        return

    if response == "NICK":
        client.send(username.encode('utf-8'))
        response = client.recv(4096).decode('utf-8')

    print(f"  {p}✓{R} Connected")

    room_code = None
    my_color = None
    join_code = os.environ.get("LINK_JOIN_CODE")
    create_room = os.environ.get("LINK_CREATE")

    if join_code:
        spinner(theme, f"Joining {join_code}...", 0.8)
        client.send(f"JOIN:{join_code}".encode('utf-8'))
        resp = client.recv(4096).decode('utf-8')
        if resp.startswith("JOINED:"):
            parts = resp.split(":")
            room_code = parts[1]
            my_color = parts[2] if len(parts) > 2 else None
            if my_color and my_color in COLOR_CODES:
                user_colors[username] = COLOR_CODES[my_color]
            print(f"  {p}✓{R} Joined {B}{room_code}{R}")
        elif resp == "BAD_CODE":
            error("Room not found.", "Check the code. It's 6 characters like A7X3KP.")
            client.close()
            return

    elif create_room:
        spinner(theme, "Creating room...", 0.8)
        client.send("CREATE:".encode('utf-8'))
        resp = client.recv(4096).decode('utf-8')
        if resp.startswith("CREATED:"):
            parts = resp.split(":")
            room_code = parts[1]
            my_color = parts[2] if len(parts) > 2 else None
            if my_color and my_color in COLOR_CODES:
                user_colors[username] = COLOR_CODES[my_color]
            show_invite(theme, room_code)

    elif response.startswith("ROOM_LIST:"):
        show_menu(theme)

        while True:
            choice = input(f"  {p}›{R} {B}Choose:{R} ").strip()

            if choice == "1":
                spinner(theme, "Creating room...", 0.8)
                client.send("CREATE:".encode('utf-8'))
                resp = client.recv(4096).decode('utf-8')
                if resp.startswith("CREATED:"):
                    parts = resp.split(":")
                    room_code = parts[1]
                    my_color = parts[2] if len(parts) > 2 else None
                    if my_color and my_color in COLOR_CODES:
                        user_colors[username] = COLOR_CODES[my_color]
                    show_invite(theme, room_code)
                break

            elif choice == "2":
                code = input(f"  {p}›{R} {B}Enter code:{R} ").strip().upper()
                if not code:
                    error("Code can't be empty.")
                    continue
                spinner(theme, f"Joining {code}...", 0.8)
                client.send(f"JOIN:{code}".encode('utf-8'))
                resp = client.recv(4096).decode('utf-8')
                if resp.startswith("JOINED:"):
                    parts = resp.split(":")
                    room_code = parts[1]
                    my_color = parts[2] if len(parts) > 2 else None
                    if my_color and my_color in COLOR_CODES:
                        user_colors[username] = COLOR_CODES[my_color]
                    print(f"  {p}✓{R} Joined {B}{room_code}{R}")
                    break
                elif resp == "BAD_CODE":
                    error("Room not found.", "Double-check the code.")
                    continue

            elif choice == "3":
                spinner(theme, "Joining latest...", 0.8)
                client.send("JOIN_LATEST".encode('utf-8'))
                resp = client.recv(4096).decode('utf-8')
                if resp.startswith("JOINED:"):
                    parts = resp.split(":")
                    room_code = parts[1]
                    my_color = parts[2] if len(parts) > 2 else None
                    if my_color and my_color in COLOR_CODES:
                        user_colors[username] = COLOR_CODES[my_color]
                    print(f"  {p}✓{R} Joined {B}{room_code}{R}")
                    break
                elif resp == "NO_ROOMS":
                    error("No rooms yet.", "Create one first.")
                    continue

            elif choice.lower() == 'q':
                client.close()
                return

            else:
                error("Pick 1, 2, 3, or q.")

    elif response == "NO_ROOMS":
        print(f"\n  {DIM}No rooms yet.{R}")
        choice = input(f"  {p}›{R} {B}Create one? (y/n):{R} ").strip().lower()
        if choice in ('y', 'yes'):
            spinner(theme, "Creating room...", 0.8)
            client.send("CREATE:".encode('utf-8'))
            resp = client.recv(4096).decode('utf-8')
            if resp.startswith("CREATED:"):
                parts = resp.split(":")
                room_code = parts[1]
                my_color = parts[2] if len(parts) > 2 else None
                if my_color and my_color in COLOR_CODES:
                    user_colors[username] = COLOR_CODES[my_color]
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
            if len(parts) > 3:
                color_map = parts[3]
                for pair in color_map.split(","):
                    if ":" in pair:
                        n, c = pair.split(":", 1)
                        if c in COLOR_CODES:
                            user_colors[n] = COLOR_CODES[c]
            show_chat_header(theme, code, username, count)
    except (ConnectionResetError, OSError):
        pass

    recv_thread = threading.Thread(target=receive_messages, args=(theme, client, username), daemon=True)
    recv_thread.start()

    send_messages(theme, client, username)


if __name__ == "__main__":
    run_client()
