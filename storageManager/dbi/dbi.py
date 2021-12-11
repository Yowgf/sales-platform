"""dbi class

dbi stands for 'database interface'
"""

import logging
import psycopg2

from config.config import config
from keys import keys

class dbi:
    def __init__(self, Config):
        self.cfg = Config
        self.connOptsStr = config.parseConnOptsSpaces(self.cfg.connOpts)

        self.connStr = (
            "user={} password={} host={} port={} dbname={} {}".
                format(
                    self.cfg.user,
                    self.cfg.password,
                    self.cfg.host,
                    self.cfg.port,
                    self.cfg.database,
                    self.connOptsStr,
                )
        )

        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(self.connStr)

    def close(self):
        self.conn.close()

    def query(self, queryStr):
        logging.debug("Querying database with string: {}".format(queryStr))
        cur = self.conn.cursor()
        cur.execute(queryStr)
        self.conn.commit()
        results = []
        if "SELECT" in queryStr and cur.rowcount > 0:
            results = cur.fetchall()
        cur.close()
        return results

################################################################
# Useful query patterns
################################################################

    def dropTable(self, tableName):
        self.query(f"DROP TABLE IF EXISTS {tableName}")

    def createTable(self, tableName, colSpec):
        createQuery = f"CREATE TABLE IF NOT EXISTS {tableName}"
        createQuery += "("
        for (colName, colType) in zip(colSpec.keys(), colSpec.values()):
            createQuery += "{} {},".format(colName, colType)
        createQuery = createQuery[:-1] # Remove last comma
        createQuery += ")"
        self.query(createQuery)

    # Raises exception if table does not exist
    def pingTable(self, tableName):
        self.query(f"SELECT * from {tableName} LIMIT 0")

    def selectStar(self, tableName):
        return self.query(f"SELECT * FROM {tableName}")

    def selectStarWhereEqual(self, tableName, conditionMap):
        queryStr = "SELECT * FROM {} WHERE ".format(tableName)
        cmkeys = conditionMap.keys()
        for (i, k, v) in zip(range(len(cmkeys)), cmkeys, conditionMap.values()):
            if i > 0:
                queryStr += "AND "
            if isinstance(v, int) or isinstance(v, float):
                queryStr += "{} = {} ".format(k, v)
            else:
                queryStr += "{} = '{}' ".format(k, v)
        return self.query(queryStr)

################################################################
# Registering for storageManager objects (case, user, etc)
################################################################

    def registerCase(self, case):
        assignedToEmail = ""
        if case.assignedTo != None:
            assignedToEmail = case.assignedTo.email
        queryStr = "INSERT INTO {} VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
            keys.caseTable,
            case.caseId,
            case.createdBy.email,
            assignedToEmail,
            case.title,
            case.category,
            case.description,
        ) + " ON CONFLICT DO NOTHING"
        self.query(queryStr)

    def registerUser(self, user):
        queryStr = "INSERT INTO {} VALUES ('{}', '{}', '{}', '{}')".format(
            keys.userTable,
            user.email,
            user.name,
            user.type,
            user.password,
        ) + " ON CONFLICT DO NOTHING"
        self.query(queryStr)

    def registerComment(self, comm):
        queryStr = "INSERT INTO {} (createdBy, createdAt, comment) \
            VALUES ('{}', '{}', '{}')".format(
            keys.commentTable,
            comm.createdBy.email,
            comm.createdAt.formalStr(),
            comm.comment,
        ) + " ON CONFLICT DO NOTHING"
        self.query(queryStr)

    def registerCaseStatus(self, status):
        queryStr = "INSERT INTO {} (status) VALUES ('{}')".format(
            keys.caseStatusTable,
            status.status,
        ) + " ON CONFLICT DO NOTHING"
        self.query(queryStr)
