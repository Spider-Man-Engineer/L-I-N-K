<div align="center">

# 🔗 L.I.N.K.

**L**ive **I**nstant **N**etwork **K**ommunication

A lightweight, terminal-based chat application with room invite codes. Built in Python with zero dependencies.

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Python 3](https://img.shields.io/badge/Python-3-blue.svg)](https://www.python.org/)
[![Homebrew](https://img.shields.io/badge/Install-Homebrew-orange.svg)](#install)

</div>

---

## Features

- 🏠 **Room system** — create private rooms with unique 6-character invite codes
- 🔗 **Share codes** — send the code to anyone to let them join
- 👥 **Multi-client** — unlimited users per room
- ⚡ **Real-time** — instant messaging over TCP
- 🖥️ **CLI interface** — interactive menu or direct commands
- 🎨 **Green UI** — clean, animated terminal interface
- 📦 **Homebrew install** — one command to install
- 🔧 **Zero dependencies** — Python 3 only, standard library

## Install

### Homebrew

```sh
brew tap SyntaxSlayerr/L-I-N-K https://github.com/SyntaxSlayerr/L-I-N-K.git
brew install link
```

### Manual

```sh
git clone https://github.com/SyntaxSlayerr/L-I-N-K.git
cd L-I-N-K
chmod +x install.sh
./install.sh
```

Then add to your shell profile:

```sh
export PATH="$HOME/.local/bin:$PATH"
```

## Usage

### Start the server

```sh
lnk server
```

### Create a room

```sh
lnk create
```

```
  ╔═════════════════════════════════╗
  ║  Room created!
  ║
  ║  Invite code:  A7X3KP
  ║
  ║  Share this code with friends
  ║  so they can join your room
  ╚═════════════════════════════════╝
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
  ┌─────────────────────────────────┐
  │  1)  Create a new room          │
  │  2)  Join by invite code        │
  │  3)  Join latest room           │
  │  q)  Quit                       │
  └─────────────────────────────────┘
```

### All Commands

| Command | Description |
|---------|-------------|
| `lnk server` | Start the chat server |
| `lnk create` | Create a room and get an invite code |
| `lnk join <CODE>` | Join a room by invite code |
| `lnk start` | Open the interactive menu |
| `lnk help` | Show help message |

## How Invites Work

1. **Host** runs `lnk server` to start the server
2. **User A** runs `lnk create` → gets a 6-char invite code
3. **User A** shares the code with friends
4. **User B** runs `lnk join A7X3KP` → joins the same room
5. Rooms auto-delete when the last person leaves

## Network Setup

By default, the server only accepts connections from your own machine (localhost).

To let friends on your LAN join, start the server with your local IP:

```sh
LINK_HOST=192.168.1.50 lnk server
```

Or set it in your shell profile:

```sh
export LINK_HOST=192.168.1.50
export LINK_PORT=5000
```

Then others on your network can connect with `lnk join <CODE>`.

## Project Structure

```
L-I-N-K/
├── lnk              # CLI entry point
├── server.py        # Chat server with room management
├── client.py        # Chat client with invite flow
├── install.sh       # Installer
├── uninstall.sh     # Uninstaller
├── build.sh         # Homebrew tarball builder
├── LICENSE          # MIT License
├── CONTRIBUTING.md  # Contribution guide
└── homebrew-link/
    └── Formula/
        └── link.rb  # Homebrew formula
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to get started.

## Uninstall

```sh
./uninstall.sh
```

Or via Homebrew:

```sh
brew uninstall link
brew untap SyntaxSlayerr/L-I-N-K
```

## License

[MIT](LICENSE)

---

<div align="center">

**Made with ❤️ for the terminal community**

⭐ Star this repo if you find it useful!

</div>
