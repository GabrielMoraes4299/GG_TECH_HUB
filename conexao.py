import mysql.connector

class Connection:
    def conectar():
        myBD = mysql.connector.connect(
            host = "",
            user="",
            password="",
            database=""
        )

        return myBD