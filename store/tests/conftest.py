import pytest
from rest_framework.test import APIClient
from core.models import User
import datetime
from store.models import *
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def api_client():
  return APIClient()


@pytest.fixture
def authenticate(api_client):
  def do_authenticate(is_staff=False):
    return api_client.force_authenticate(user=User(is_staff=is_staff))
  return do_authenticate


@pytest.fixture
def user_set():
  return User.objects.create(
    username = 'sam332',
    password = '33333333332',
    email = 's2s@gmail.com',
    first_name = 'sm2',
    last_name = 'ff2',
    is_staff = False,
    is_superuser = False,
    is_active = True,
    date_joined = datetime.datetime(2023,11,11,5,45,3).strftime("%Y-%m-%dT%H:%M:%SZ")
  )

  
  
@pytest.fixture
def collection_set():
  return Collection.objects.create(
    title = 'Costumes'
  )
  
  
@pytest.fixture
def product_set(collection_set):
  return Product.objects.create(
    title='Kitkat',
    description='Chocolate',
    unit_price=22,
    inventory=1,
    collection=collection_set
  )
  
  
@pytest.fixture
def cart_set():
  return Cart.objects.create()


@pytest.fixture
def cart_item_set(product_set,cart_set):
  cart = CartItem.objects.create(product=product_set,quantity=2,cart=cart_set)
  return cart


@pytest.fixture
def order_set(api_client,cart_item_set,user_set):
  token = AccessToken.for_user(user_set)
  api_client = APIClient()
  api_client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
  
  orderset = api_client.post('/api/orders/',{'cart_id':cart_item_set.cart_id})
  order = Order.objects.get(id=orderset.data['id'])
  
  return order