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

    def query(self):
        pass
