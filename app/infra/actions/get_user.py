from app.infra.configs import DBConnector
from app.infra.entities import UsersTable
from uuid import UUID

def get_username(user_uuid: str):
    with DBConnector() as db:
        results = db.session.query(UsersTable.user).filter(UsersTable.userUuid == user_uuid).scalar()
    
    return results