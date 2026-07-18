import io
import zipfile


def start_session(client, folder_name="minha-pasta", total_files=1) -> str:
    resp = client.post(
        "/api/upload/start",
        data={"folder_name": folder_name, "total_files": total_files},
    )
    assert resp.status_code == 200
    return resp.json()["session_id"]


def send_file(client, session_id, relative_path, content: bytes):
    return client.post(
        f"/api/upload/{session_id}/file",
        data={"relative_path": relative_path},
        files={"file": (relative_path.split("/")[-1], io.BytesIO(content))},
    )


def test_full_upload_download_cycle(client):
    session_id = start_session(client, "docs", total_files=2)

    resp = send_file(client, session_id, "sub/a.txt", b"conteudo A")
    assert resp.status_code == 200
    assert resp.json() == {"uploaded": 1, "total": 2}

    resp = send_file(client, session_id, "b.txt", b"BB")
    assert resp.status_code == 200

    resp = client.post(f"/api/upload/{session_id}/complete")
    assert resp.status_code == 200
    body = resp.json()
    assert body["total_files"] == 2
    assert body["total_size"] == len(b"conteudo A") + len(b"BB")

    # Listagem de pastas
    resp = client.get("/api/folders")
    folders = resp.json()
    assert len(folders) == 1
    assert folders[0]["original_name"] == "docs"

    # Árvore de arquivos
    resp = client.get(f"/api/folders/{session_id}/files")
    assert resp.status_code == 200
    tree = resp.json()["tree"]
    names = {child["name"] for child in tree["children"]}
    assert names == {"sub", "b.txt"}

    # Download individual preserva o conteúdo
    resp = client.get(f"/api/folders/{session_id}/file", params={"path": "sub/a.txt"})
    assert resp.status_code == 200
    assert resp.content == b"conteudo A"

    # Download ZIP da pasta inteira
    resp = client.get(f"/api/folders/{session_id}/download")
    assert resp.status_code == 200
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        assert sorted(zf.namelist()) == ["b.txt", "sub/a.txt"]
        assert zf.read("sub/a.txt") == b"conteudo A"

    # Exclusão da pasta limpa banco e listagem
    resp = client.delete(f"/api/folders/{session_id}")
    assert resp.status_code == 200
    assert client.get("/api/folders").json() == []


def test_chunked_upload_reassembles_file(client):
    session_id = start_session(client, "grande", total_files=1)
    part1, part2 = b"primeira-metade|", b"segunda-metade"
    total = len(part1) + len(part2)

    for index, chunk in enumerate([part1, part2]):
        resp = client.post(
            f"/api/upload/{session_id}/file-chunk",
            data={
                "relative_path": "video.bin",
                "chunk_index": index,
                "total_chunks": 2,
                "total_size": total,
            },
            files={"file": ("video.bin", io.BytesIO(chunk))},
        )
        assert resp.status_code == 200

    resp = client.get(f"/api/folders/{session_id}/file", params={"path": "video.bin"})
    assert resp.content == part1 + part2

    resp = client.get("/api/folders")
    assert resp.json()[0]["total_size"] == total


def test_upload_rejects_path_traversal(client):
    session_id = start_session(client)
    resp = send_file(client, session_id, "../fora.txt", b"x")
    assert resp.status_code == 400


def test_download_rejects_path_traversal(client):
    session_id = start_session(client)
    send_file(client, session_id, "ok.txt", b"x")
    resp = client.get(
        f"/api/folders/{session_id}/file", params={"path": "../../segredo.txt"}
    )
    assert resp.status_code == 400


def test_unknown_session_and_folder_return_404(client):
    resp = send_file(client, "nao-existe", "a.txt", b"x")
    assert resp.status_code == 404
    assert client.get("/api/folders/nao-existe/files").status_code == 404
    assert client.get("/api/folders/nao-existe/download").status_code == 404
    assert client.delete("/api/folders/nao-existe").status_code == 404


def test_files_search_pagination_and_delete(client):
    session_id = start_session(client, "misc", total_files=3)
    send_file(client, session_id, "relatorio.pdf", b"%PDF")
    send_file(client, session_id, "foto.jpg", b"\xff\xd8")
    send_file(client, session_id, "notas/relatorio-final.pdf", b"%PDF2")

    # Busca por trecho do caminho
    resp = client.get("/api/files", params={"q": "relatorio"})
    body = resp.json()
    assert body["total"] == 2
    assert {f["name"] for f in body["files"]} == {
        "relatorio.pdf",
        "relatorio-final.pdf",
    }

    # Paginação
    resp = client.get("/api/files", params={"limit": 2})
    assert resp.json()["total"] == 3
    assert len(resp.json()["files"]) == 2

    # Exclusão de arquivo individual atualiza contadores da pasta
    file_id = body["files"][0]["id"]
    assert client.delete(f"/api/files/{file_id}").status_code == 200
    assert client.get("/api/files", params={"q": "relatorio"}).json()["total"] == 1

    folder = client.get("/api/folders").json()[0]
    assert folder["total_files"] == 2


def test_download_batch_zips_only_selected(client):
    session_id = start_session(client, "lote", total_files=3)
    send_file(client, session_id, "a.txt", b"A")
    send_file(client, session_id, "b.txt", b"B")
    send_file(client, session_id, "c.txt", b"C")

    resp = client.post(
        f"/api/folders/{session_id}/download-batch",
        json={"paths": ["a.txt", "c.txt", "../malicioso.txt"]},
    )
    assert resp.status_code == 200
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        assert sorted(zf.namelist()) == ["a.txt", "c.txt"]
