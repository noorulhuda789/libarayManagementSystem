# Library Management System

This repository hosts a Library Management System (LMS) developed in Python using PyQt5 for the graphical user interface. The project focuses on user and book management within a library setting.

## Features

- **Book Management**: Catalog, add, edit, and delete books from the library inventory.
- **Borrower Management**: Manage borrower information, issue library cards, and track borrowing history.
- **Fine Management**: Track fines accrued by borrowers for late returns.
- **User Management**: Administer user access levels and permissions within the system.

## Custom Data Structures

This project includes custom-designed data structures and algorithms tailored for efficient book and borrower management, optimizing processes like book cataloging, borrowing, and fine tracking.

## Installation and Setup

### Prerequisites

Ensure you have Python installed. If not, download and install it from [Python's official website](https://www.python.org/).

### Dependencies

Make sure you have the following packages installed:

- **PyQt5**: Python bindings for Qt toolkit used for the graphical user interface.

You can install PyQt5 and its dependencies using `pip`:

```bash
pip install PyQt5
```

### Running the Application
To run the Library Management System, follow these steps:

Clone this repository to your local machine:

```bash
git clone https://gitlab.com/alsabur20/dsafinalprojectpid31
```
Navigate to the project directory:

```bash
cd dsafinalprojectpid31
```
Modify the main path in the main.py file with your folder path:

Open the main.py file in a text editor and find the mainpath variable. Update the mainpath variable to reflect the path to your project directory. For example:

```python
mainpath = r"C:\Users\YourUsername\Path\to\dsafinalprojectpid31"
```
Run the main application file:
```bash
python main.py
```
This will start the application and launch the graphical user interface for the Library Management System.

### Contributing
We welcome contributions! If you'd like to contribute to this project, please fork the repository, make your changes, and submit a pull request.