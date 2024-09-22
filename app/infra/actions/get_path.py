from app.infra.configs import DBConnector
from app.infra.entities import FilesTable
from uuid import UUID

def get_file_path_and_name(file_uuid: str):
    with DBConnector() as db:
        file_uuid = format_int_as_uuid(file_uuid)
        path, name, ftype = db.session.query(FilesTable.file_path, FilesTable.file_name, FilesTable.file_type).filter(FilesTable.fileUuid == file_uuid).first()
    
    return path, name + ftype

def format_int_as_uuid(number):
    hex_str = f"{number:032x}"
    formatted_uuid = f"{hex_str[:8]}-{hex_str[8:12]}-{hex_str[12:16]}-{hex_str[16:20]}-{hex_str[20:]}"

    return UUID(formatted_uuid)
