import sqlite3


class Database:
    def __init__(self, path_to_db="data/main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            number INTEGER PRIMARY KEY AUTOINCREMENT,
            id INTEGER NOT NULL,
            Name VARCHAR(255) NOT NULL,
            time TEXT NOT NULL,
            username VARCHAR(255)
            );
        """
        self.execute(sql, commit=True)

    def create_table_reviews(self):
        sql = """
        CREATE TABLE Reviews (
            number INTEGER PRIMARY KEY AUTOINCREMENT,
            id INTEGER NOT NULL,
            Name VARCHAR(255) NOT NULL,
            time TEXT NOT NULL,
            review TEXT NOT NULL,
            username VARCHAR(255)
            );
        """
        self.execute(sql, commit=True)

    def create_table_statistics(self):
        sql = """
                CREATE TABLE Statistics (
                id INTEGER PRIMARY KEY DEFAULT 1,
                fail INTEGER NOT NULL DEFAULT 1,
                victory INTEGER NOT NULL DEFAULT 1
                );
                """
        self.execute(sql, commit=True)

    def set_table_statistics(self):
        self.execute("INSERT INTO Statistics(id, fail, victory) VALUES(1, 0, 0);", commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, time: str, username: str = None):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, username, time) VALUES(1, 'John', 'john', '2020-12-07 22:03:07')"
        sql = """
        INSERT INTO Users(id, Name, time, username) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, time, username), commit=True)

    def add_review(self, id: int, name: str, time: str, review: str, username: str = None):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, time, review, username)
        sql = """
        INSERT INTO Reviews(id, Name, time, review, username) VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, time, review, username), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_all_reviews(self):
        sql = """
        SELECT * FROM Reviews
        """
        return self.execute(sql, fetchall=True)

    def get_statistics(self):
        sql = """
           SELECT fail, victory FROM Statistics
           """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_review(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Reviews WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_numbers_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def count_numbers_reviews(self):
        return self.execute("SELECT COUNT(*) FROM Reviews;", fetchone=True)

    def delete_numbers_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def delete_numbers_reviews(self):
        self.execute("DELETE FROM Reviews WHERE TRUE", commit=True)

    def add_fail(self):
        self.execute("UPDATE Statistics SET fail = fail + 1", commit=True)

    def add_victory(self):
        self.execute("UPDATE Statistics SET victory = victory + 1", commit=True)


def logger(statement):
    print(f"""
    _____________________________________________________        
    Executing: 
    {statement}
    _____________________________________________________
    """)
