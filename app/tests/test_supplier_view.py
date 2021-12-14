from fastapi.testclient import TestClient
from starlette import responses


def test_supplier_create(client: TestClient):
    response = client.post('/supplier/', json={
        'name': 'Fornecedor 1'
    })

    assert response.status_code == 201
    assert response.json()['id'] == 1


def test_supplier_update(client: TestClient):
    response = client.post('/supplier/', json={
        'name': 'Fornecedor 1'
    })

    assert response.status_code == 201

    response = client.put(
        '/supplier/1', json={'name': 'Novo Fornecedor 1'}
    )

    assert response.status_code == 200
    assert response.json()['name'] == 'Novo Fornecedor 1'