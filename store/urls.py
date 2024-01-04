from .views import *
from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register('products',ProductViewSet,basename='product')
product_router = routers.NestedDefaultRouter(router,'products',lookup='product')
product_router.register('reviews',ReviewViewSet,basename='product-reviews')
product_router.register('images',ProductImageViewSet,basename='product-images')

router.register('collections',CollectionViewSet,basename='collection')

router.register('carts',CartViewSet,basename='cart')
cart_router = routers.NestedDefaultRouter(router,'carts',lookup='carts')
cart_router.register('items',CartItemViewSet,basename='cart-items')

router.register('customers',CustomerViewSet,basename='customer')
address_router = routers.NestedDefaultRouter(router,'customers',lookup='customers')
address_router.register('address',AddressViewSet,basename='customer-address')

router.register('orders',OrderViewSet,basename='order')


urlpatterns = router.urls + product_router.urls + cart_router.urls + address_router.urls