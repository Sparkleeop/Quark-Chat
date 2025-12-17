# Quark Chat CLI

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-stable-success)

A lightweight terminal-based chat application built using Python sockets and threads.
Designed for local networks or small deployments, Quark Chat CLI prioritizes simplicity, clarity, and a minimal protocol while still supporting practical real-world features.

---

## Overview

Quark Chat CLI consists of a TCP server and a command-line client that enable real-time communication directly from the terminal.
Each connected user is assigned a distinct color, messages are broadcast in order, and the server maintains basic shared state such as active users and recent chat history.

The project intentionally avoids external frameworks and dependencies to keep the networking, concurrency, and protocol logic explicit and easy to understand.

---

## Features

* Multi-client chat over TCP sockets
* Threaded server with concurrent connection handling
* Username validation and collision prevention
* Colorized usernames for improved readability
* Private messaging between users
* Server-side announcements
* Chat history replay for new connections
* Message length limiting
* Timestamped server-side logging
* Graceful resource cleanup on shutdown

---

## Commands

### Client Commands

```
/pm <username> <message>   Send a private message
/history                  View recent chat history
/shrug                    Send ¯\_(ツ)_/¯
/exit                     Leave the chat
```

### Server Commands

```
/stats                    Display server statistics
/users                    List connected users
/announce <message>       Broadcast a server announcement
/help                     Show available commands
```

---

## Project Structure

```
.
├── server.py   TCP chat server
├── client.py   CLI chat client
└── logs/       Server log files
```

Log files are written with timestamps and include user joins, disconnects, public messages, private messages, and announcements.

---

## Running the Server

```bash
python server.py
```

The server listens on all network interfaces (`0.0.0.0`) using port `5000` by default.

---

## Running a Client

```bash
python client.py
```

By default, the client connects to `127.0.0.1:5000`.
Users are prompted to select a unique username on connection.

---

## Technical Notes

* Each client connection is handled in its own thread.
* Shared server state is protected using a threading lock to prevent race conditions.
* Messages are newline-delimited for simplicity.
* ANSI escape codes are used for terminal color output.
* The architecture is intentionally synchronous and blocking for predictability and clarity.

---

## Limitations

* No encryption or authentication
* Not intended for internet-facing or production deployments
* No persistent storage beyond server logs
* Terminal rendering may vary across platforms

---

## Motivation

Quark Chat CLI was built as a practical exercise in:

* socket programming
* concurrency and synchronization
* lightweight protocol design
* state management
* CLI-based application development

The project emphasizes transparency and direct control over abstraction-heavy approaches.

---

## License

This project is provided under the MIT License for educational and experimental use.
  
> **NOTE** This README was generated with AI assistance.
