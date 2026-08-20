# 🔗 link

A lightweight, terminal-based chat application built with Python 💬. Spin up a server, connect as many clients as you want, and chat in real time — all from the command line.

## ✨ Features

- 🖥️ Simple CLI interface
- ⚡ Real-time messaging
- 👥 Multi-client support
- 🏠 Self-hosted — run on your own machine or LAN
- 📦 Installable via Homebrew or manual setup
- 🔧 Zero dependencies — uses only the Python standard library

## 📥 Install

### 🍺 Homebrew

```sh
brew tap nerf/link
brew install link
```

### 🔧 Manual

```sh
git clone https://github.com/nerf/link.git
cd link
chmod +x install.sh
./install.sh
```

Make sure `~/.local/bin` is in your `PATH`:

```sh
export PATH="$HOME/.local/bin:$PATH"
```

## 🚀 Usage

### 1. Start the server

```sh
lnk server
```

You should see:

```
Server is running on port 5000...
```

### 2. Connect a client

Open another terminal (or another machine on the same network) and run:

```sh
lnk start
```

Enter a username when prompted and start chatting! 🎉

### 3. Disconnect

Type `quit` to leave the chat.

## 🗑️ Uninstall

```sh
./uninstall.sh
```

## 📁 Project Structure

```
link/
├── lnk          # CLI entry point
├── server.py    # Chat server
├── client.py    # Chat client
├── install.sh   # Installer
├── uninstall.sh # Uninstaller
├── build.sh     # Build script for Homebrew formula
└── homebrew-link/
    └── Formula/
        └── link.rb
```

## 📝 License

MIT
