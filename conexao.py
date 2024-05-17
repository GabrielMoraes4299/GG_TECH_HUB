import mysql.connector

class Connection:
    def conectar():
        myBD = mysql.connector.connect(
            host = "127.0.0.1",
            user="equipe",
            password="123456789",
            database="bd_ggtech"
        )

        return myBD