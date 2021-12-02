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
