import socket
import threading
import sys
import os

DEFAULT_HOST = os.environ.get("LINK_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("LINK_PORT", "5000"))


def show_banner():
    print("""
  _          _ _
 | |    __ _| | | __ _
 | |   / _` | | |/ _` |
 | |__| (_| | | | (_| |
 |_____\__,_|_|_|\__,_|
    """)


def show_menu():
    print("  1) Create a new room")
    print("  2) Join by invite code")
    print("  3) Join latest room")
    print("  q) Quit")
    print()


def receive_messages(client):
    while True:
        try:
            message = client.recv(4096).decode('utf-8')
            if not message:
                print("\n🔌 Disconnected from server.")
                client.close()
                break
            print(f"\r{message}")
        except:
            print("\n🔌 Connection lost.")
            client.close()
            break


def send_messages(client, username):
    while True:
        try:
            msg = input()
            if msg.lower() == 'quit':
                client.close()
                sys.exit(0)
            client.send(msg.encode('utf-8'))
        except:
            break


def run_client(host=DEFAULT_HOST, port=DEFAULT_PORT):
    show_banner()

    username = input("  Enter your username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except ConnectionRefusedError:
        print(f"\n  ❌ Could not connect to {host}:{port}")
        print("  Make sure the server is running: lnk server\n")
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
        client.send(f"JOIN:{join_code}".encode('utf-8'))
        resp = client.recv(4096).decode('utf-8')
        if resp.startswith("JOINED:"):
            room_code = resp.split(":", 1)[1]
            print(f"\n  ✅ Joined room {room_code}!\n")
        elif resp == "BAD_CODE":
            print(f"  ❌ Invalid invite code: {join_code}")
            client.close()
            return

    elif create_room:
        client.send("CREATE:".encode('utf-8'))
        resp = client.recv(4096).decode('utf-8')
        if resp.startswith("CREATED:"):
            room_code = resp.split(":", 1)[1]
            print(f"\n  ✅ Room created!")
            print(f"  🔗 Invite code: {room_code}")
            print(f"  Share this code with friends to let them join!\n")

    elif response.startswith("ROOM_LIST:"):
        codes = response.split(":", 1)[1].split(",") if response.split(":", 1)[1] else []
        print()
        show_menu()

        while True:
            choice = input("  Choose: ").strip()

            if choice == "1":
                client.send("CREATE:".encode('utf-8'))
                resp = client.recv(4096).decode('utf-8')
                if resp.startswith("CREATED:"):
                    room_code = resp.split(":", 1)[1]
                    print(f"\n  ✅ Room created!")
                    print(f"  🔗 Invite code: {room_code}")
                    print(f"  Share this code with friends to let them join!\n")
                break

            elif choice == "2":
                code = input("  Enter invite code: ").strip().upper()
                client.send(f"JOIN:{code}".encode('utf-8'))
                resp = client.recv(4096).decode('utf-8')
                if resp.startswith("JOINED:"):
                    room_code = resp.split(":", 1)[1]
                    print(f"\n  ✅ Joined room {room_code}!\n")
                    break
                elif resp == "BAD_CODE":
                    print("  ❌ Invalid code. Try again.")
                    continue

            elif choice == "3":
                client.send("JOIN_LATEST".encode('utf-8'))
                resp = client.recv(4096).decode('utf-8')
                if resp.startswith("JOINED:"):
                    room_code = resp.split(":", 1)[1]
                    print(f"\n  ✅ Joined room {room_code}!\n")
                    break
                elif resp == "NO_ROOMS":
                    print("  ❌ No active rooms. Create one first.")
                    continue

            elif choice.lower() == 'q':
                client.close()
                return

    elif response == "NO_ROOMS":
        print()
        print("  📭 No active rooms.")
        choice = input("  Create one? (y/n): ").strip().lower()
        if choice == 'y':
            client.send("CREATE:".encode('utf-8'))
            resp = client.recv(4096).decode('utf-8')
            if resp.startswith("CREATED:"):
                room_code = resp.split(":", 1)[1]
                print(f"\n  ✅ Room created!")
                print(f"  🔗 Invite code: {room_code}")
                print(f"  Share this code with friends to let them join!\n")
        else:
            client.close()
            return

    info = client.recv(4096).decode('utf-8')
    if info.startswith("ROOM_INFO:"):
        parts = info.split(":")
        code = parts[1]
        count = parts[2]
        print(f"  📡 Room {code} — {count} user(s) online\n")

    recv_thread = threading.Thread(target=receive_messages, args=(client,), daemon=True)
    recv_thread.start()

    send_messages(client, username)


if __name__ == "__main__":
    run_client()
