import pytest
from rest_framework import status
from store.models import *

@pytest.fixture
def handle_orders(api_client,order_set):
  def do_handle_orders(cart_id,method=None):
    if method == 'patch':
      return api_client.patch(f'/api/orders/{order_set.pk}/',cart_id)
    if method == 'delete':
      return api_client.delete(f'/api/orders/{order_set.pk}/')
    return api_client.post('/api/orders/',cart_id)
  return do_handle_orders


@pytest.mark.django_db
class TestOrders:
  def test_if_user_is_anonymous_returns_401(self,handle_orders):
    response = handle_orders({'cart_id':''})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
  
  def test_if_user_is_authenticated_and_data_is_invalid_returns_400(self,handle_orders,authenticate):
    authenticate()
    
    response = handle_orders({'cart_id':''})
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
  
  def test_if_user_is_authenticated_and_data_is_valid_returns_200(self,cart_item_set,user_set,api_client):
    api_client.force_authenticate(user_set)
    
    response = api_client.post('/api/orders/',{'cart_id':cart_item_set.cart_id})
    
    assert response.status_code == status.HTTP_200_OK
    
    
  def test_if_not_admin_and_update_returns_403(self,authenticate,handle_orders):
    authenticate()
    
    response = handle_orders({'payment_status':'C'},'patch')
    
    assert response.status_code == status.HTTP_403_FORBIDDEN

  
  def test_if_admin_and_update_data_is_valid_returns_200(self,authenticate,handle_orders):
    authenticate(is_staff=True)
    
    response = handle_orders({'payment_status':'C'},'patch')
    
    assert response.status_code == status.HTTP_200_OK
      
    
  def test_if_admin_and_update_data_is_invalid_returns_400(self,authenticate,handle_orders):
    authenticate(is_staff=True)
    
    response = handle_orders({'payment_status':'G'},'patch')

    assert response.status_code == status.HTTP_400_BAD_REQUEST  
    
    
  def test_if_admin_and_delete_is_not_allowed_returns_405(self,authenticate,handle_orders):
    authenticate(is_staff=True)
    
    response = handle_orders(None,'delete')
    
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.data.get('detail') is not None
    