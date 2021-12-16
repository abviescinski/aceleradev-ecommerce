from fastapi.testclient import TestClient


def test_category_create(client: TestClient, admin_auth_header):
    response = client.post('/category/', headers=admin_auth_header,
                           json={'name': 'Categoria 1'})

    assert response.status_code == 201
    assert response.json()['id'] == 1


def test_category_update(client: TestClient, category_factory, admin_auth_header):
    category = category_factory()

    response = client.put(
        f'/category/{category.id}', headers=admin_auth_header,
        json={'name': 'Categoria alterada'})

    assert response.status_code == 200
    assert category.name == 'Categoria alterada'


def test_category_get_all(client: TestClient, category_factory, admin_auth_header):
    category = category_factory()
    
    response = client.get('/category/', headers=admin_auth_header)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_category_get_id(client: TestClient, category_factory, admin_auth_header):
    category = category_factory()

    response = client.get(f'/category/{category.id}', headers=admin_auth_header)

    assert response.status_code == 200
    assert response.json()['name'] == category.name
