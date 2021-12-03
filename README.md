# Group

- Alexander Thomas Mol Holmquist
- Breno Claudio de Sena Pimenta
- Gabriel Henrique Dias Neves
- Larissa Dolabella Gomide

# sales-platform

Platform for a sales team to manage client cases.

# How to run

Simply pass `main.py` to the python interpreter, and the program should start.

In linux:

```shell
python3 main.py
```

In Windows (not tested):

```shell
python main.py
```

# Code overview

The code is divided into two parts: userInterface (front end) and storageManager (_kind of_ a back end).

Currently, the storageManager just contains some mock data for the users, and does not persist memory in any way. In the future, we would like to include some kind of database connection, so that data is persisted through application runs.

Furthermore, the only way to access the application at the moment is through the console.

# Technology overview
 
During the developement of the code, we choosed to use Python version 3.8 or above, and Pytest framework for tests. The tests run automatically when upload new code to Github, or it can run localy using

```
python -m pytest
```
or

```
pytest
```