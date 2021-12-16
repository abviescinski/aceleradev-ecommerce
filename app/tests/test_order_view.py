from fastapi.testclient import TestClient


def test_order_create(client: TestClient, address_factory, payment_method_factory,
                      coupon_factory, product_factory, customer_auth_header):
    address = address_factory()
    payment_method = payment_method_factory()
    coupon = coupon_factory()
    product = product_factory()
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
    print(response.headers)
    assert response.status_code == 201
    assert len(response.json()) == 1
