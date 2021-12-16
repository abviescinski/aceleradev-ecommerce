from fastapi.testclient import TestClient


def test_supplier_create(client: TestClient, admin_auth_header):
    response = client.post('/supplier/', headers=admin_auth_header,
                           json={'name': 'Fornecedor 1'})

    assert response.status_code == 201
    assert response.json()['id'] == 1


def test_supplier_get(client: TestClient, supplier_factory, admin_auth_header):
    supplier = supplier_factory()

    response = client.get('/supplier/', headers=admin_auth_header)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == supplier.name


def test_supplier_update(client: TestClient, supplier_factory, admin_auth_header):
    supplier = supplier_factory()

    response = client.put(f'/supplier/{supplier.id}',
                          headers=admin_auth_header, json={'name': 'Novo Fornecedor 1'})

    assert response.status_code == 200
    assert supplier.name == 'Novo Fornecedor 1'


def test_supplier_get_id(client: TestClient, supplier_factory, admin_auth_header):
    supplier = supplier_factory()

    response = client.get(f'/supplier/{supplier.id}', headers=admin_auth_header)

    assert response.status_code == 200
    assert response.json()['name'] == supplier.name
