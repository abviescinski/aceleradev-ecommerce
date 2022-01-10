from fastapi.testclient import TestClient
from datetime import datetime, timedelta


def test_order_create(client: TestClient, address_factory, payment_method_factory,
                      coupon_factory, product_factory, customer_auth_header):
    address = address_factory()
    payment_method = payment_method_factory()
    coupon = coupon_factory()
    product = product_factory()
    print(customer_auth_header)
    response = client.post('/order/', headers=customer_auth_header,
                           json={
                               "address_id": address.id,
                               "payment_method_id": payment_method.id,
                               "coupon_code": coupon.code,
                               "products": [
                                   {
                                       "quantity": 2,
                                       "product_id": product.id
                                   }
                               ]})
    assert response.status_code == 201


def test_order_create_role_admin(client: TestClient, address_factory, payment_method_factory,
                                 coupon_factory, product_factory, admin_auth_header):
    address = address_factory()
    payment_method = payment_method_factory()
    coupon = coupon_factory()
    product = product_factory()
    response = client.post('/order/', headers=admin_auth_header,
                           json={
                               "address_id": address.id,
                               "payment_method_id": payment_method.id,
                               "coupon_code": coupon.code,
                               "products": [
                                   {
                                       "quantity": 2,
                                       "product_id": product.id
                                   }
                               ]})
    assert response.status_code == 403


def test_order_status_initial_order_placed(client: TestClient, order_factory, admin_auth_header):
    order = order_factory()
    response = client.get('/order/', headers=admin_auth_header)
    assert response.status_code == 200
    assert response.json()[0]['status'] == 'ORDER PLACED'


def test_order_total_value(client: TestClient, address_factory, payment_method_factory,
                           coupon_factory, product_factory, customer_auth_header, admin_auth_header):
    address = address_factory()
    payment_method = payment_method_factory()
    coupon = coupon_factory()
    product = product_factory()
    product2 = product_factory()
    response = client.post('/order/', headers=customer_auth_header,
                           json={
                               "address_id": address.id,
                               "payment_method_id": payment_method.id,
                               "coupon_code": coupon.code,
                               "products": [
                                   {
                                       "quantity": 2,
                                       "product_id": product.id
                                   },
                                   {
                                       "quantity": 3,
                                       "product_id": product2.id
                                   }
                               ]})

    assert response.status_code == 201

    response = client.get('/order/', headers=admin_auth_header)
    price = float((product.price * 2) + (product2.price*3))

    assert response.json()[0]['total_value'] == price

    # testar o calculo da percentagem


def test_order_coupon_invalid(client: TestClient, address_factory, payment_method_factory,
                              coupon_factory, product_factory, customer_auth_header):
    # código inválido
    address = address_factory()
    payment_method = payment_method_factory()
    product = product_factory()
    response = client.post('/order/', headers=customer_auth_header,
                           json={
                               "address_id": address.id,
                               "payment_method_id": payment_method.id,
                               "coupon_code": "CodigoInvalido",
                               "products": [
                                   {
                                       "quantity": 2,
                                       "product_id": product.id
                                   },
                               ]})

    assert response.status_code == 404
    assert response.json() == {'detail': 'Informations not found.'}

    # data inválida
    coupon = coupon_factory(expire_at=datetime.now()-timedelta(days=10))
    response = client.post('/order/', headers=customer_auth_header,
                           json={
                               "address_id": address.id,
                               "payment_method_id": payment_method.id,
                               "coupon_code": coupon.code,
                               "products": [
                                {
                                    "quantity": 2,
                                    "product_id": product.id
                                },
                               ]})

    assert response.status_code == 400
    assert response.json()['detail'] == "Coupon Invalid."

    # quantidade esgotada #TODO não implementei no app ainda
    """
    coupon = coupon_factory(limit=1)
    response = client.post('/order/', headers=customer_auth_header,
                        json={
                            "address_id": address.id,
                            "payment_method_id": payment_method.id,
                            "coupon_code": coupon.code,
                            "products": [
                                {
                                    "quantity": 2,
                                    "product_id": product.id
                                },
                            ]})

    assert response.status_code == 201

    response2 = client.post('/order/', headers=customer_auth_header,
                json={
                    "address_id": address.id,
                    "payment_method_id": payment_method.id,
                    "coupon_code": coupon.code,
                    "products": [
                        {
                            "quantity": 2,
                            "product_id": product.id
                        },
                    ]})
    
    assert response2.status_code == 400
    assert response2.json()['detail'] == "Coupon Invalid."
    """

    # código do produto inexistente

    # quantidade do produto indisponivel

    # status order inexistente

    # tentar inserir uma order com um número já existente
