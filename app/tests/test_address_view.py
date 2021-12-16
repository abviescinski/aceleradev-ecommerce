from fastapi.testclient import TestClient

'''
def test_address_create(client: TestClient, admin_auth_header):
    response = client.post('/address/', headers=admin_auth_header,
                           json={'name': 'Categoria 1'})

    assert response.status_code == 201
    assert response.json()['id'] == 1


def test_address_update(client: TestClient, address_factory, admin_auth_header):
    address = address_factory()

    response = client.put(
        f'/address/{address.id}', headers=admin_auth_header,
        json={'name': 'Categoria alterada'})

    assert response.status_code == 200
    assert address.name == 'Categoria alterada'


def test_address_get_all(client: TestClient, address_factory, admin_auth_header):
    address = address_factory()
    
    response = client.get('/address/', headers=admin_auth_header)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_address_get_id(client: TestClient, address_factory, admin_auth_header):
    address = address_factory()

    response = client.get(f'/address/{address.id}', headers=admin_auth_header)

    assert response.status_code == 200
    assert response.json()['name'] == address.name
'''