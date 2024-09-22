from app.infra.configs import DBConnector, Base

def init_data_base():
    with DBConnector() as db:
        Base.metadata.create_all(db.session.bind)