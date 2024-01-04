import pytest
from rest_framework import status

@pytest.fixture
def handle_products(api_client,product_set):
  def do_handle_products(products,method=None):
    if method == 'geta':
      return api_client.get(f'/api/products/')
    if method == 'getd':
      return api_client.get(f'/api/products/{product_set.pk}/')
    if method == 'put':
      return api_client.put(f'/api/products/{product_set.pk}/',products)
    if method == 'patch':
      return api_client.patch(f'/api/products/{product_set.pk}/',products)
    if method == 'delete':
      return api_client.delete(f'/api/products/{product_set.pk}/')
    return api_client.post('/api/products/',products)
  return do_handle_products


@pytest.mark.django_db
class TestProducts:
  def test_if_data_list_view_returns_200(self,handle_products):
    response = handle_products(None,'geta')
    
    assert response.status_code == status.HTTP_200_OK
    
    
  def test_if_data_detail_view_returns_200(self,handle_products):
    response = handle_products(None,'getd')
    
    assert response.status_code == status.HTTP_200_OK


  def test_if_data_is_valid_returns_201(self,handle_products,collection_set):
    response = handle_products({
      'title':'Kitkat',
      'description':'Chocolate',
      'unit_price':22,
      'inventory':1,
      'collection':collection_set.pk
    })
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['id'] > 0
    
    
  def test_if_data_is_invalid_returns_400(self,handle_products):
    response = handle_products({
      'title':'',
      'description':'',
      'unit_price':'',
      'inventory':'',
      'collection':''
    })
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    assert response.data['title'] is not None
    assert response.data['description'] is not None
    assert response.data['unit_price'] is not None
    assert response.data['inventory'] is not None
    assert response.data['collection'] is not None


  def test_if_update_data_is_valid_returns_200(self,handle_products,collection_set):
    response = handle_products({
      'title':'Kitkat',
      'description':'Chocolate',
      'unit_price':24,
      'inventory':1,
      'collection':collection_set.pk
    },'put')
    
    assert response.status_code == status.HTTP_200_OK
    
    
  def test_if_partial_update_data_is_valid_returns_200(self,handle_products):
    response = handle_products({
      'title':'Kitkat',
      'description':'Milk Shake',
    },'patch')
    
    assert response.status_code == status.HTTP_200_OK
    
    
  def test_if_delete_data_is_valid_returns_200(self,handle_products):
    response = handle_products(None,'delete')
    
    assert response.status_code == status.HTTP_204_NO_CONTENT