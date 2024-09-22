from app.infra.configs import DBConnector
from app.infra.entities import UsersTable
from sqlalchemy import select
import bcrypt

class Login:
    def __init__(self, user: str, password: str):
        self.user = user
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.userUuid = None

    def login(self):
        with DBConnector() as db:
            user = db.session.execute(select(UsersTable).where(UsersTable.user == self.user)).scalar()
        
        if user is None:
            return False

        self.userUuid = user.userUuid
        
        return bcrypt.checkpw(self.password.encode('utf-8'), user.password.encode('utf-8')), str(user.id)

    def get_uuid(self):
        return self.userUuid