import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """TestClient com banco SQLite e pasta all_files isolados em tmp_path.

    A pasta all_files usa Path relativo resolvido a cada request, então o
    chdir basta para ela. O banco precisa de um engine próprio por teste
    (com caminho absoluto), senão todos os testes compartilham o arquivo
    criado no primeiro import de database.py.
    """
    monkeypatch.chdir(tmp_path)

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    import database
    import main

    engine = create_engine(
        f"sqlite:///{tmp_path / 'transferencia.db'}",
        connect_args={"check_same_thread": False},
    )
    monkeypatch.setattr(database, "engine", engine)
    monkeypatch.setattr(
        database,
        "SessionLocal",
        sessionmaker(autocommit=False, autoflush=False, bind=engine),
    )
    monkeypatch.setattr(main, "engine", engine)

    from fastapi.testclient import TestClient

    with TestClient(main.app) as c:
        yield c

    engine.dispose()
