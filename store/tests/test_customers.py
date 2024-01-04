from rest_framework import status
import pytest
import datetime

@pytest.fixture
def handle_customers(api_client,user_set):
  def do_handle_customers(collection,method=None):
    if method == 'g':
      return api_client.get('/api/customers/')
    elif method == 'p':
      return api_client.put(f'/api/customers/{user_set.pk}/',collection)
    elif method == 'p-me':
      return api_client.get(f'/api/customers/me/')
    return api_client.post('/api/customers/',collection)
  return do_handle_customers


@pytest.mark.django_db
class TestCustomers:
  def test_if_user_is_anonymous_returns_401(self,handle_customers):
    response = handle_customers({'phone':'a'})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    
  def test_if_user_is_not_admin_returns_403(self,authenticate,handle_customers):
    authenticate()
    
    response = handle_customers({'phone':'sssss'})
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
    
  def test_if_data_is_invalid_returns_400(self,authenticate,handle_customers):
    authenticate(is_staff=True)
    
    response = handle_customers({'phone':''})
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['phone'] is not None
    
  
  def test_if_admin_and_update_data_is_valid_returns_200(self,authenticate,handle_customers):
    authenticate(is_staff=True)

    response = handle_customers(
      {
        'phone':'333',
        'birth_date':datetime.date(2023,11,11)
      },"p"
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] > 0 
    
    
  def test_if_authenticated_and_returns_200(self,user_set,api_client):
    api_client.force_authenticate(user_set)
    
    response = api_client.get('/api/customers/me/')
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] > 0 
    
    
  def test_if_authenticated_and_update_data_is_valid_returns_200(self,user_set,api_client):
    api_client.force_authenticate(user_set)
    
    response = api_client.patch('/api/customers/me/',{'phone': '334123'})
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['phone'] == '334123'