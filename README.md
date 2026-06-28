# 📚 Library Management System

A production-ready Command Line Interface (CLI) application built using **Python 3.14**, **SQLAlchemy 2.0** type-hinted annotations, and a local **SQLite** database layer. 

This project demonstrates clean database architecture, modular code separation, bidirectional relationships, and strict data validation constraints.

---

## 🏗️ System Architecture & Database Design

The application is fully decoupled across four logical modules to ensure high testability, clean separation of concerns, and zero thread-locking issues:

1. **`models.py`**: Defines the object-relational mapping (ORM) schema using modern `Mapped` and `mapped_column` styles.
2. **`crud.py`**: Encapsulates all transactional persistence logic (Create, Read, Update, Delete) isolated away from interface input/output parsing.
3. **`seed.py`**: A deployment utility script to instantly purge, re-verify, and populate the database with mock benchmarking metrics.
4. **`main.py`**: The terminal-driven user interface and controller loop.

### Entity-Relationship Design Highlights
* **Many-to-Many Bridge**: Books and Authors are dynamically mapped via a secondary `book_author` association table, allowing an individual book to support multiple authors.
* **Elevated Association Entity**: The `Borrowing` record functions as a distinct operational model class rather than a simple lookup link. This enables the schema to store critical live metadata attributes such as specific checkout timestamps and nullable return dates.

---

## ⚡ Features & Data Integrity Validation

* **Automated Seed Utility**: Populates the schema instantly with 3 authors, 5 books, 4 library members, and 6 complex historical/active transaction rows.
* **Strict Inventory Control**: Prevents a book checkout transaction from proceeding if the current remaining `available_copies` drops to `0`.
* **Relational Deletion Blocks**: Enforces strong domain-level referential protection constraints. The application explicitly blocks the deletion of any member or book entity that is actively associated with an outstanding, unreturned loan record.
* **Overdue Tracking Engine**: Built-in calculation engine that flags unreturned books exceeding the library's standard 14-day return window.

---

## 🚀 Installation & Local Execution

### Prerequisites
* Python 3.13+ or 3.14 (managed cleanly via `uv` or standard virtual environments)

### 1. Set Up Your Environment
Clone the repository, open your terminal inside the root project directory, and ensure your dependencies are installed:
```bash
# If using vanilla pip
pip install -r requirements.txt

# If utilizing uv environment paths
uv pip install -r requirements.txt
