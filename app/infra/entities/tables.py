from app.infra.configs import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

class UsersTable(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    userUuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    user = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class FilesTable(Base):
    __tablename__ = 'Files'

    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    fileUuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    ower = Column(Integer, ForeignKey('Users.id'), nullable=False)