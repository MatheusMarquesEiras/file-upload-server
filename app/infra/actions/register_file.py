from app.infra.configs import DBConnector
from app.infra.entities import UsersTable, FilesTable
from sqlalchemy import select
import os

class RegisterFile:
    def __init__(self, filename: str, fileUuid: str, fileExtension: str, userUuid: str):
        self.filename = filename
        self.fileUuid = fileUuid
        self.file_type = fileExtension
        self.file_path = os.path.join('uploads', userUuid, str(self.fileUuid) + self.file_type)
        with DBConnector() as db:
            self.ower = db.session.execute(select(UsersTable.id).where(UsersTable.userUuid == userUuid)).scalar()

    def register(self):
        with DBConnector() as db:
            new_file = FilesTable(file_name=self.filename, file_type=self.file_type, file_path=self.file_path, fileUuid=self.fileUuid, ower=self.ower)
            db.session.add(new_file)
            db.session.commit()