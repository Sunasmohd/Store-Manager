from rest_framework import status
import pytest

@pytest.fixture
def handle_collection(api_client,collection_set):
  def do_handle_collection(collection,method=None):
    if method == 'geta':
      return api_client.get('/api/collections/')
    if method == 'getd':
      return api_client.get(f'/api/collections/{collection_set.pk}/')
    if method == 'put':
      return api_client.put(f'/api/collections/{collection_set.pk}/',collection)
    if method == 'delete':
      return api_client.delete(f'/api/collections/{collection_set.pk}/')
    return api_client.post('/api/collections/',collection)
  return do_handle_collection


@pytest.mark.django_db
class TestCreateCollection:
  def test_if_user_is_anonymous_returns_401(self,handle_collection):
    response = handle_collection({'title':'a'})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    
  def test_if_user_is_not_admin_returns_403(self,authenticate,handle_collection):
    authenticate()
    
    response = handle_collection({'title':'sssss'})
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
    
  def test_if_data_is_invalid_returns_400(self,authenticate,handle_collection):
    authenticate(is_staff=True)
    
    response = handle_collection({'title':''})
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['title'] is not None
    
    
  def test_if_admin_and_data_list_view_returns_200(self,authenticate,handle_collection):
    authenticate(is_staff=True)
    
    response = handle_collection(None,'geta')
    
    assert response.status_code == status.HTTP_200_OK
    
    
  def test_if_admin_and_data_detail_view_returns_200(self,authenticate,handle_collection):
    authenticate(is_staff=True)
    
    response = handle_collection(None,'getd')
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] is not None

    
  def test_if_admin_and_data_is_valid_returns_201(self,authenticate,handle_collection):
    authenticate(is_staff=True)
    
    response = handle_collection({'title':'c'})
    
    assert response.status_code == status.HTTP_201_CREATED
    # assert Collection.objects.get(id=response.data['id'])
    assert response.data['id'] > 0    #right approach
    
    
  def test_if_admin_and_data_is_invalid_returns_200(self,authenticate,handle_collection):
    authenticate(is_staff=True)
    
    response = handle_collection({'title':''})
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['title'] is not None
    
  
  def test_if_admin_and_update_data_is_valid_returns_200(self,authenticate,handle_collection):
    authenticate(is_staff=True)
    
    response = handle_collection({'title':'aa'},'put')
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'aa'
 
    
  def test_if_admin_and_delete_data_returns_204(self,authenticate,handle_collection):
    authenticate(is_staff=True)
    
    response = handle_collection(None,'delete')
    
    assert response.status_code == status.HTTP_204_NO_CONTENT