# 🔗 Link

> **L**ive **I**nstant **N**etwork **K**ommunication

A lightweight, terminal-based chat app with **room invite codes**. Spin up a server, create rooms, share the code, and your friends can join from anywhere on the network.

## ✨ Features

- 🏠 **Room system** — create private rooms with unique 6-char invite codes
- 🔗 **Share codes** — send the code to anyone to let them join
- 👥 **Multi-client** — unlimited users per room
- ⚡ **Real-time** — instant messaging over TCP
- 🖥️ **CLI interface** — interactive menu or direct commands
- 📦 **Homebrew install** — one command to install
- 🔧 **Zero dependencies** — Python 3 only, standard library

## 📥 Install

### 🍺 Homebrew (macOS / Linux)

```sh
brew tap Spider-Man-Engineer/link
brew install link
```

### 🔧 Manual

```sh
git clone https://github.com/Spider-Man-Engineer/L-I-N-K.git
cd L-I-N-K
chmod +x install.sh
./install.sh
```

Then add to your shell profile:

```sh
export PATH="$HOME/.local/bin:$PATH"
```

## 🚀 Usage

### Start the server

```sh
lnk server
```

### Create a room

```sh
lnk create
```

Output:

```
  ✅ Room created!
  🔗 Invite code: A7X3KP
  Share this code with friends to let them join!
```

### Join by invite code

```sh
lnk join A7X3KP
```

### Interactive menu

```sh
lnk start
```

```
  1) Create a new room
  2) Join by invite code
  3) Join latest room
  q) Quit

  Choose:
```

### All commands

| Command | Description |
|---------|-------------|
| `lnk server` | Start the chat server |
| `lnk create` | Create a room and join it |
| `lnk join <CODE>` | Join a room by invite code |
| `lnk start` | Open the interactive menu |
| `lnk help` | Show help message |

## 🔗 How Invites Work

1. **Host** runs `lnk server` to start the server
2. **User A** runs `lnk create` — gets a 6-char invite code (e.g. `A7X3KP`)
3. **User A** shares the code with friends
4. **User B** runs `lnk join A7X3KP` — joins the same room
5. Rooms auto-delete when the last person leaves

## 🌐 Network Setup

To let friends on your LAN join, use your local IP:

```sh
LINK_HOST=192.168.1.50 lnk start
```

Or set it in your shell profile:

```sh
export LINK_HOST=192.168.1.50
export LINK_PORT=5000
```

## 📁 Project Structure

```
L-I-N-K/
├── lnk              # CLI entry point
├── server.py        # Chat server with room management
├── client.py        # Chat client with invite flow
├── install.sh       # Installer
├── uninstall.sh     # Uninstaller
├── build.sh         # Homebrew tarball builder
└── homebrew-link/
    └── Formula/
        └── link.rb  # Homebrew formula
```

## 🗑️ Uninstall

```sh
./uninstall.sh
```

Or via Homebrew:

```sh
brew uninstall link
brew untap Spider-Man-Engineer/link
```

## 📝 License

MIT
