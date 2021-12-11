from config.config import config
from storageManager.user.user import user
from storageManager.case.case import case

def sampleConfig():
    return config([
        "-host=127.0.0.1",
        "-port=1521",
        "-database=exampleDatabase",
        "-user=exampleUser",
        "-password=examplePassword",
        "-connOpts=sslmode=disable",
    ])

def sampleUsers():
    return {
            "daniel@email.com": user("daniel@email.com", "Daniel", "customer", "password321"),
            "joseph@email.com": user("joseph@email.com", "Joseph", "sales", "password123"),
            "c": user("c", "c", "customer", "c"),
            "s": user("s", "s", "sales", "s"),
    }

def sampleCase():
    return (case("exampleId", "exampleCreator").
        populate("exampleTitle", "exampleCategory", "exampleDescription")
    )

def sampleUser():
    return user("exampleEmail", "exampleName", "sales", "examplePassword")
