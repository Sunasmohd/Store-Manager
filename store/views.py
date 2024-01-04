from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from rest_framework.generics import *
from .serializers import *
from rest_framework import status
from django.db.models.aggregates import Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from uuid import UUID


class ProductImageViewSet(ModelViewSet):
  serializer_class = ProductImageSerialzier
  
  def get_queryset(self):
    return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
  
  def get_serializer_context(self):
    return {'product_id' : self.kwargs['product_pk']}


class ProductViewSet(ModelViewSet):
  queryset = Product.objects.prefetch_related('images','promotions').all()
  serializer_class = ProductSerializer
  filter_backends = [DjangoFilterBackend]
  filterset_fields = ['collection_id']
  
  def get_serializer_context(self):
      return {'request':self.request}
    
  def destroy(self,request,*args,**kwargs):
      if OrderItem.objects.filter(product_id=kwargs['pk']):
        return Response({'error' : "Can't delete this product.Associated with an order"},status=status.HTTP_400_BAD_REQUEST)
      return super().destroy(request,*args,**kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
                product_count = Count('products')
              )
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def destroy(self,request,*args,**kwargs):
      if Product.objects.filter(collection_id=kwargs['pk']):
        return Response({'error' : "Can't delete this collection.Associated with a product"},status=status.HTTP_400_BAD_REQUEST)
      return super().destroy(request,*args,**kwargs)
    

class ReviewViewSet(ModelViewSet):
  serializer_class = ReviewSerializer
  
  def get_queryset(self):
     return Reviews.objects.filter(product_id=self.kwargs['product_pk'])
     
  def get_serializer_context(self):
     return {'product_id' : self.kwargs['product_pk']}
  
  
class CartViewSet(ModelViewSet):
  http_method_names = ('get','post','delete','head','options')
  serializer_class = CartSerializer
  queryset = Cart.objects.all()
  
  def get_queryset(self):
    if self.request.user.is_superuser:
      return Cart.objects.prefetch_related('items__product').all()
    else:
      sess = self.request.session.get('cart_id')
      if sess:
        cart=Cart.objects.filter(id=UUID(sess))
        return cart
      elif self.request.user.is_authenticated:
          return Cart.objects.filter(user_id=self.request.user.id)
      else:
          return Cart.objects.none()
        
          
  def create(self, request, *args, **kwargs):
      serializer = CartSerializer(data=request.data, 
                                  context={'user_id': request.user.id,
                                           'cart_id':request.session.get('cart_id') or None
                                          })
      serializer.is_valid(raise_exception=True)
      cart_id = serializer.save()
      
      if not request.user.is_authenticated:
          request.session['cart_id'] = str(cart_id.id)
      else:
        sess = request.session.get('cart_id')
        if sess:
          Cart.objects.filter(user_id=request.user.id).filter(id=UUID(sess), user__isnull=True).update(user_id=request.user.id)
          del request.session['cart_id']
          
      return Response(serializer.data)
    
      
  def destroy(self, request, *args, **kwargs):
    if 'cart_id' in request.session:
      del request.session['cart_id']
    instance = get_object_or_404(Cart,pk=kwargs.get('pk'))
    self.perform_destroy(instance)
    return Response(status=status.HTTP_204_NO_CONTENT)
  
class CartItemViewSet(ModelViewSet):
  http_method_names = ['get','post','patch','delete'] ## small letter must
  
  def get_serializer_context(self):
     return {'cart_id':self.kwargs['carts_pk']}
  
  def get_serializer_class(self):
     if self.request.method == 'POST':
       return CreateCartItemSerializer
     if self.request.method == 'PATCH':
       return UpdateCartItemSerializer
     return CartItemSerializer
  
  def get_queryset(self):
     return CartItem.objects.filter(cart_id=self.kwargs['carts_pk']).select_related('product')
   
   
class CustomerViewSet(ModelViewSet):
  queryset = Customer.objects.all()
  serializer_class = CustomerSerializer
  permission_classes = [permissions.IsAdminUser]

  
  @action(detail=False,methods=['GET','PATCH'],permission_classes = [permissions.IsAuthenticated])
  def me(self,request):
    customer = Customer.objects.get(user_id=request.user.id)
    
    if request.method == 'GET':
      serializer = CustomerSerializer(customer)
      return Response(serializer.data)
    elif request.method == 'PATCH':
      serializer = CustomerSerializer(customer,data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data)


class AddressViewSet(ModelViewSet):
  serializer_class = AddressSerializer
  
  def get_queryset(self,*args,**kwargs):
    return Address.objects.filter(customer_id=self.kwargs.get('customers_pk'))
  
  def get_serializer_context(self):
    return {'customer_id':self.kwargs.get('customers_pk')}


class OrderViewSet(ModelViewSet):
  http_method_names = ('patch','get','post','head','options')
  
  def get_permissions(self):
    if self.request.method in ('PATCH'):
      return [permissions.IsAdminUser()]
    return [permissions.IsAuthenticated()]
  
  def get_serializer_class(self):
    if self.request.method == 'POST':
      return CreateOrderSerializer
    elif self.request.method == 'PATCH':
      return UpdateOrderSerializer
    return OrderSerializer
  
  def create(self, request, *args, **kwargs):
    serializer = CreateOrderSerializer(data=request.data,context={'user_id':self.request.user.id,'cart_session':self.request.session.get('cart_id')})
    serializer.is_valid(raise_exception=True)
    order = serializer.save()
    serializer = OrderSerializer(order)
    return Response(serializer.data)
    
  def get_queryset(self):
    if self.request.user.is_staff:
      return Order.objects.all() 
    customer_id = Customer.objects.get(user_id=self.request.user.id)
    return Order.objects.filter(customer_id=customer_id)   
  
  def destroy(self,request,*args,**kwargs):
    if OrderItem.objects.filter(order_id=kwargs['pk']):
      return Response({'error' : "Can't delete this order.Associated with a orderitem"},status=status.HTTP_400_BAD_REQUEST)
    return super().destroy(request,*args,**kwargs)
  
  
class OrderItemViewSet(ModelViewSet):
  queryset = OrderItem.objects.all()
  serializer_class = OrderItemSerializer