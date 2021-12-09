"""config class"""

import yaml

from utils.utils import safeMapVal

from .errors.malformedFlag import malformedFlag
from .errors.malformedConnOpts import malformedConnOpts
from .errors.nonExistantFlag import nonExistantFlag
from .errors.missingFlags import missingFlags

class config:
    flags = ["host", "port", "database", "user", "password", "connOpts"]
    requiredFlags = ["host", "port", "database", "user", "password"]

    def sampleConfig():
        return config([
            "-host=127.0.0.1",
            "-port=1521",
            "-database=exampleDatabase",
            "-user=exampleUser",
            "-password=examplePassword",
            "-connOpts=sslmode=disable",
        ])

    def __init__(self, configArg):
        self.C = {}

        self.host = ""
        self.port = ""
        self.database = ""
        self.user = ""
        self.password = ""
        self.connOpts = ""

        # Parse from list of arguments
        if isinstance(configArg, list):
            self.C = config.parseList(configArg)
        # Parse from yaml file
        if isinstance(configArg, str):
            self.C = config.parseFile(configArg)
        
        self.setConfig(self.C)

        self.checkMissingFlags(self.C)

    # The argument list is given in the form '-flag=value'
    def parseList(arglist):
        C = {}

        for arg in arglist:
            if len(arg) > 0 and arg[0] == '-':
                arg = arg[1:]

                flagValue = arg.split("=")

                if len(flagValue) < 2:
                    raise malformedFlag(arg)

                flag = flagValue[0]
                value = "=".join(flagValue[1:])

                if flag not in config.flags:
                    raise nonExistantFlag(arg)
                if value == "":
                    raise malformedFlag(arg)

                # Build C piece by piece
                C[flag] = value
        return C

    def parseFile(configFilePath):
        C = None
        with open(configFilePath) as f:
            C = yaml.load(f, Loader=yaml.FullLoader)

        return C

    def setConfig(self, C):
        self.host = safeMapVal(C, "host")
        self.port = safeMapVal(C, "port")
        self.database = safeMapVal(C, "database")
        self.user = safeMapVal(C, "user")
        self.password = safeMapVal(C, "password")
        self.connOpts = safeMapVal(C, "connOpts")

    def checkMissingFlags(self, C):
        # Build a message containing all missing flags
        missingFlagsMessage = ""

        ckeys = C.keys()
        for flag in self.requiredFlags:
            if flag not in ckeys:
                missingFlagsMessage += flag + ","
        
        if missingFlagsMessage != "":
            # Disconsider last comma
            missingFlagsMessage = missingFlagsMessage[:-1]
            raise missingFlags(missingFlagsMessage)

    # Parse connection options on the format 'opt1=val1,opt2=val2,...' to a map.
    def parseConnOptsMap(connOpts):
        M = {}
        flagValues = connOpts.split(",")
        for i in range(len(flagValues)):
            flagValue = flagValues[i].split("=")

            if len(flagValue) != 2:
                raise malformedConnOpts(connOpts)
            
            flag = flagValue[0]
            val = flagValue[1]

            M[flag] = val

    # Parse connection options to the format "opt1=val1 opt2=val2 ..."
    def parseConnOptsSpaces(connOpts):
        return connOpts.replace(",", " ")

    # Parse connection options to the format "?opt1=val1&opt2=val2&..."
    def parseConnOptsUrl(connOpts):
        parsedConnOpts = ""

        M = config.parseConnOptsMap(connOpts)
        mkeys = list(M.keys())
        for i in range(len(mkeys)):
            if i == 0:
                parsedConnOpts += "?"
            else:
                parsedConnOpts += "&"
            
            parsedConnOpts += M[mkeys[i]]

        return parsedConnOpts
