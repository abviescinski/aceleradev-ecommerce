import factory
from fastapi.testclient import TestClient
from starlette import responses


def test_product_create(client: TestClient, category_factory, supplier_factory, admin_auth_header):
    category = category_factory()
    supplier = supplier_factory()
    response = client.post('/product/', headers=admin_auth_header,
                           json={'description': 'descricao',
                                 'price': 100,
                                 'image': 'image.dev',
                                 'technical_details': 'bla bla',
                                 'visible': True,
                                 'category_id': category.id,
                                 'supplier_id': supplier.id
                                 })
    assert response.status_code == 201
    assert response.json()['description'] == 'descricao'
    assert response.json()['category_id'] == category.id
    assert response.json()['supplier_id'] == supplier.id


def test_product_update(client: TestClient, product_factory, admin_auth_header):
    product = product_factory()
    response = client.put(f'/product/{product.id}', headers=admin_auth_header,
                          json={'description': 'Nova descricao',
                                'price': product.price,
                                'image': product.image,
                                'technical_details': 'bla bla',
                                'visible': True,
                                'category_id': product.category.id,
                                'supplier_id': product.supplier.id
                                })
    assert response.status_code == 200
    assert product.description == 'Nova descricao'



def test_product_get_all(client: TestClient, product_factory, admin_auth_header):
    product = product_factory()

    response = client.get('/product/', headers=admin_auth_header)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_product_get_id(client: TestClient, product_factory, admin_auth_header):
    product = product_factory()

    response = client.get(f'/product/{product.id}', headers=admin_auth_header)

    assert response.status_code == 200
    assert response.json()['description'] == product.description
