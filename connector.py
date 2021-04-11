import pyodbc


class Connector:
    def __init__(self, database_url):
        conn = pyodbc.connect(database_url)
        self.cursor = conn.cursor()

    def execute(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def execute(self, sql_query):
        rows = self.cursor.execute(sql_query).fetchall()
        records = [tuple(map(str, record)) for record in rows]
        accessfile = set(records)