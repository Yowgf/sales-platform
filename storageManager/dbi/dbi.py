"""dbi class

dbi stands for 'database interface'
"""

import psycopg2

from config.config import config

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
        cur = self.conn.cursor()
        cur.execute(queryStr)
        results = None
        if cur.rowcount > 0:
            results = cur.fetchall()
        cur.close()
        return results

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
