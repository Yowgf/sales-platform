# Sales Platform

Platform for a sales team to manage client cases.

# Group

- Alexander Thomas Mol Holmquist
- Breno Claudio de Sena Pimenta
- Gabriel Henrique Dias Neves
- Larissa Dolabella Gomide

# How to run

Simply pass `main.py` to the python interpreter, and the program should start.

In linux:

```shell
python3 main.py
```

In Windows:

```shell
python main.py
```

# Code overview

The software simulates a platform that clients and sellers exchange messages about a case that need to be solved by the seller's team. It is possible to assign cases between the team and to change the status of the cases while it being solved. The clients can rate the sellers every time they send a message to them. It is possible to check each seller average rating. 

Since the focus is for testing a software, the interface is really simple and runs on the console. The code is divided into two parts: userInterface (front end) and storageManager (_kind of_ a back end).

Currently, the storageManager just contains some mock data for the users, and does not persist memory in any way. In the future, we would like to include some kind of database connection, so that data is persisted through application runs.

Furthermore, the only way to access the application at the moment is through the console.

To use the application use the following login information:

Seller Login:
```
user: s
passwaord: s
```

Client Login:
```
user: c
passwaord: c
```

# Technology overview
 
During the developement of the code, we choosed to use Python version 3.8 or above, and Pytest framework for tests. The tests run automatically when upload new code to Github, or it can run localy using

```
python -m pytest
```
or

```
pytest
```

The workflow is configured to run tests on MacOS, Windows and Ubuntu.

![Build Status](https://img.shields.io/appveyor/build/Yowgf/sales-platform)

[![](https://img.shields.io/appveyor/tests/Yowgf/sales-platform)