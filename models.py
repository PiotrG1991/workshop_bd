from bcrypt import hash_password

class users:
    def __init__(self, username=" ", password=" ", salt=None):
        self._id = -1
        self._username = username
        self._hashed_password = hash_password(password, salt)


    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)
    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users (username, hashed_password)
                    VALUES (%s, %s) RETURNING id"""
            values = (self._username, self._hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()
            return True
        return False

    @staticmethod
    def load_user_by_username(cursor, username):
        sql = """ SELECT id, username, hashed_password FROM users WHERE username = %s"""
        cursor.execiute(sql, (username,))
        data = cursor.fetchall()
        if data:
            id_, username, hashed_password = data
            loaded_user = users(username)
            loaded_user._id = id_
            loaded_user.hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_user_by_id(self, cursor):
        sql = " SELECT id, username, hashed_password FROM users WHERE id = %s"
        cursor.execute(sql, (self._id,))
        data = cursor.fetchall()
        if data:
            id_, username, hashed_password = data
            loaded_user = users(username)
            loaded_user._id = id_
            loaded_user.hashed_password = hashed_password
            return loaded_user
        else:
            return None
            
    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM users"
        cursor.execute(sql)
        users = []
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = users
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id = %s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True


class messages:
    def __init__(self, from_id, to_id, text):
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self._creation_date = None

        @property
        def creation_date(self):
            return self._creation_date

        @property
        def id(self):
            return self._id

        @staticmethod
        def load_all_messages(cursor, user_id=None):
            if user_id:
                sql = "SELECT id, from_id, to_id, text, creation_date FROM messages WHERE to_id=%s"
                cursor.execute(sql, (user_id,))
            else:
                sql = "SELECT id, from_id, to_id, text, creation_date FROM messages"
                cursor.execute(sql)
            messages = []
            for row in cursor.fetchall():
                id_, from_id, to_id, text, creation_date = row
                loaded_message = Message(from_id, to_id, text)
                loaded_message._id = id_
                loaded_message._creation_date = creation_date
                messages.append(loaded_message)
            return messages

        def save_to_db(cursor):
            if self._id == -1:
                sql = """ INSERT INTO messages(from_id, to_id, text) 
                VALUES (%s, %s, %s) RETURNING  id, creation_date"""
                values = (self.from_id, self.to_id, self.text)
                cursor.execute(sql, values)
                self._id, self._creation_date = cursor.fetchone()
                return True
            else:
                sql = """UPDATE messages SET to_id = %s, text = %s WHERE id = %s"""
                values = (self.from_id, self.to_id, self.text, self._id)
                cursor.execute(sql, values)
                return True
