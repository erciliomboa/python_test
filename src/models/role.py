from flask_mysqldb import MySQL


class Role():

    def __init__(self, type_role, _id):
        self.type_role = type_role
        self._id = _id


    @classmethod
    def get_role(cls):
        mysql = MySQL(Role)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM role")
        Rules = cur.fetchall()
        return cls(** Rules)
