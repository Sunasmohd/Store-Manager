from rest_framework import status
import pytest


@pytest.fixture
def handle_cart(api_client,cart_set):
  def do_handle_cart(method=None):
    if method == 'delete':
      return api_client.delete(f'/api/carts/{cart_set.pk}/')
    return api_client.post('/api/carts/')
  return do_handle_cart



@pytest.fixture
def handle_cart_item(api_client,cart_set,cart_item_set):
  def do_handle_cart_item(cart_item,method=None):
    if method == 'delete':
      return api_client.delete(f'/api/carts/{cart_set.pk}/items/{cart_item_set.pk}/')
    if method == 'patch':
      return api_client.patch(f'/api/carts/{cart_set.pk}/items/{cart_item_set.pk}/',cart_item)
    return api_client.post(f'/api/carts/{cart_set.pk}/items/',cart_item)
  return do_handle_cart_item


@pytest.mark.django_db
class TestCarts:
  def test_if_data_is_valid_returns_201(self,handle_cart,cart_set):
    response = handle_cart()
    
    assert response.status_code == status.HTTP_200_OK
  
  
  def test_if_delete_data_is_valid_returns_204(self,handle_cart):
    response = handle_cart('delete')
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    

@pytest.mark.django_db
class TestCartItems:
  def test_if_data_is_invalid_returns_400(self,handle_cart_item):
    response = handle_cart_item({'cart_id':'','product_id':'','quantity':''})
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['product_id'] is not None
    assert response.data['quantity'] is not None
    
    
  def test_if_data_is_valid_returns_201(self,handle_cart_item,cart_set,product_set):
    response = handle_cart_item({'cart_id':cart_set.pk,'product_id':product_set.pk,'quantity':2})
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['id'] > 0
  
  
  def test_if_delete_data_is_valid_returns_204(self,handle_cart_item):
    response = handle_cart_item(None,'delete')
    
    assert response.status_code == status.HTTP_204_NO_CONTENT


  def test_if_partial_update_data_is_valid_returns_200(self,handle_cart_item,cart_set):
    response = handle_cart_item({'quantity':5,'cart':cart_set},'patch')
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['quantity'] == 5
