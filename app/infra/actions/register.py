from flask import current_app, session
from app.infra.configs import DBConnector
from app.infra.entities import UsersTable
from sqlalchemy import select
import bcrypt
import os


class Register:
    def __init__(self, userUuid: str, user: str, password: str):
        self.userUuid = userUuid
        self.user = user
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def register(self):
        with DBConnector() as db:
            existing_user = db.session.execute(select(UsersTable).where(UsersTable.user == self.user)).scalar_one_or_none()

            if existing_user is not None:
                return False
            
            new_user = UsersTable(userUuid=self.userUuid, user=self.user, password=self.password)
            db.session.add(new_user)
            db.session.commit()
        
            self.userUuid = new_user.userUuid
            print(self.userUuid)
            print(type(self.userUuid))

            if not os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], str(self.userUuid))):
                os.makedirs(os.path.join(current_app.config['UPLOAD_FOLDER'], str(self.userUuid)))
        
        return True
    
    def get_uuid(self):
        return self.userUuid