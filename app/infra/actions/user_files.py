from app.infra.configs import DBConnector
from app.infra.entities import UsersTable, FilesTable

def get_user_files(user_uuid: str):
    with DBConnector() as db:
        results = db.session.query(
            FilesTable.file_name, FilesTable.fileUuid
        ).join(
            UsersTable, UsersTable.id == FilesTable.ower
        ).filter(
            UsersTable.userUuid == user_uuid
        ).all()

    return list((results))