"""config class"""

import yaml

from utils.utils import setIfExists

from .errors.malformedFlag import malformedFlag
from .errors.malformedConnOpts import malformedConnOpts
from .errors.nonExistantFlag import nonExistantFlag
from .errors.missingFlags import missingFlags

class config:
    flags = ["config-file", "host", "port", "database", "user", "password", "connOpts"]
    requiredFlags = ["host", "port", "database", "user", "password"]

    def __init__(self, configArg):
        self.C = {}

        self.host = ""
        self.port = ""
        self.database = ""
        self.user = ""
        self.password = ""
        self.connOpts = ""

        # Parse from yaml file
        self.C = self.update(self.C, config.parseFile(configArg))
        
        # Parse from list of arguments
        self.C = self.update(self.C, config.parseList(configArg))

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

    def parseFile(configArg):
        configFile = "config.yaml"
        parsedList = config.parseList(configArg)
        configFile = setIfExists(configFile, parsedList, "config-file")

        C = None
        with open(configFile) as f:
            C = yaml.load(f, Loader=yaml.FullLoader)

        return C

    def update(self, old, new):
        definitive = old
        for k in new.keys():
            definitive[k] = new[k]

        self.setConfig(definitive)

        return definitive

    def setConfig(self, C):
        self.host = setIfExists(self.host, C, "host")
        self.port = setIfExists(self.port, C, "port")
        self.database = setIfExists(self.database, C, "database")
        self.user = setIfExists(self.user, C, "user")
        self.password = setIfExists(self.password, C, "password")
        self.connOpts = setIfExists(self.connOpts, C, "connOpts")

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
