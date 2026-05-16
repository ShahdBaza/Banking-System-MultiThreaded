# Multi-Threaded Banking System

A robust, concurrent Banking System built with **Python Sockets** and **Multithreading**. This project demonstrates advanced software engineering concepts, including distributed systems and design patterns.

##  Features
* **Concurrency:** Handles multiple client connections simultaneously using Python's `threading` library.
* **Socket Communication:** Reliable data exchange between the Server and multiple Clients.
* **Transaction Management:** Supports core banking operations like Deposit, Withdrawal, and Balance Inquiry.
* **Scalable Architecture:** Designed to be easily extended with new features.

##  Architecture & Design Patterns
This project focuses on clean code and the **SOLID principles**:

1. **Observer Pattern:** Used to synchronize and notify account state changes across the system.
2. **Command Pattern:** Encapsulates banking operations as objects, allowing for flexible execution and logging.
3. **Thread Safety:** Implemented to ensure data integrity during concurrent financial transactions.

##  Tech Stack
* **Language:** Python
* **Networking:** Socket Programming
* **Concurrency:** Multi-threading
* **Design Patterns:** Observer, Command

##  How to Run
1. **Start the Server:**
   ```bash
   python server.py

2.Connect a Client:
    python client.py

## 🎓 Academic Context
This project was developed as part of the **Programming 2** course during my second year of Software Engineering studies.