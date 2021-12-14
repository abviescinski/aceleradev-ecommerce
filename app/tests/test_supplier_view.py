from fastapi.testclient import TestClient


def test_supplier_create(client: TestClient):
    response = client.post('/supplier/', json={
        'name': 'Fornecedor 1'
    })

    assert response.status_code == 201
    assert response.json()['id'] == 1


def test_supplier_get(client: TestClient):
    response = client.post('/supplier/', json={
        'name': 'Fornecedor 1'
    })
    assert response.status_code == 201

    response = client.get('/supplier/')

    assert response.status_code == 200
    assert response.json()[0]['name'] == 'Fornecedor 1'


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


def test_supplier_get_id(client: TestClient):
    response = client.post('/supplier/', json={
        'name': 'Fornecedor 1'
    })
    assert response.status_code == 201

    response = client.get('/supplier/1')

    assert response.status_code == 200
    assert response.json()['name'] == 'Fornecedor 1'