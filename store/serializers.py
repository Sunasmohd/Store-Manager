from rest_framework import serializers
from .models import *
from django.db import transaction
from uuid import UUID
from django.shortcuts import get_object_or_404
  
class CollectionSerializer(serializers.ModelSerializer):
  product_count = serializers.IntegerField(read_only=True)
  class Meta:
    model = Collection
    fields = ['id','title','product_count']
    

class ProductImageSerialzier(serializers.ModelSerializer):
  class Meta:
    model = ProductImage
    fields = ['id','image']
    
  def create(self, validated_data):
    return ProductImage.objects.create(product_id=self.context['product_id'],**validated_data)
  
  
class ProductSerializer(serializers.ModelSerializer):
  images = ProductImageSerialzier(many=True,read_only=True)
  class Meta:
    model = Product
    fields = ['id','title','description','unit_price','inventory','last_update','collection',
            'images','promotions']

  
class ReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model = Reviews
    fields = ['id','name','description','date']
    
  def create(self,validated_data):
    product_id = self.context['product_id']
    return Reviews.objects.create(product_id=product_id,**validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
  class Meta:
      model = Product
      fields = ['id','title','unit_price']
      
      
class CreateCartItemSerializer(serializers.ModelSerializer):
  product_id = serializers.IntegerField()
  class Meta:
    model = CartItem
    fields = ['id','product_id','quantity']
  
  def save(self, **kwargs):
    product_id = self.validated_data.get('product_id')
    quantity = self.validated_data.get('quantity')
    cart_id = self.context['cart_id']
    try:
      cart_item = CartItem.objects.get(cart_id=cart_id,product_id=product_id)
      cart_item.quantity += quantity
      cart_item.save()
      self.instance = cart_item
    except CartItem.DoesNotExist:
      self.instance = CartItem.objects.create(cart_id=cart_id,**self.validated_data)
    return self.instance
  
  
class UpdateCartItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = CartItem
    fields = ['quantity']
      
      
class CartItemSerializer(serializers.ModelSerializer):
  product = SimpleProductSerializer()
  total_price = serializers.SerializerMethodField()
  class Meta:
    model = CartItem
    fields = ['id','quantity','product','total_price']
  
  def get_total_price(self,cart_item:CartItem):
    return cart_item.quantity * cart_item.product.unit_price
    
    
class CartSerializer(serializers.Serializer):
  items = CartItemSerializer(many=True,read_only=True)
  total_price = serializers.SerializerMethodField()
  user_id = serializers.IntegerField(read_only=True)
  id = serializers.UUIDField(read_only=True)

  def get_total_price(self,cart:Cart):
    return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
  
  def save(self, **kwargs):
    user_id = self.context.get('user_id')
    cart_id = self.context.get('cart_id')
    
    if user_id:
      try:
        self.instance = Cart.objects.get(user_id=user_id)
      except:
        if cart_id:
          self.instance = Cart.objects.get(id=cart_id)
          self.instance.user_id = user_id
          self.instance.__dict__.update(**self.validated_data)
          self.instance.save()
          return self.instance
        self.instance = Cart.objects.create(user_id=user_id,**self.validated_data)
      return self.instance
    
    elif cart_id and Cart.objects.count() > 0:
      self.instance = get_object_or_404(Cart,id=UUID(cart_id))
      return self.instance
    
    else:
      self.instance = Cart.objects.create(**self.validated_data)
    return self.instance


class AddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = Address
    fields = ['street','city','country']
    
  def save(self, **kwargs):
    customer = self.context['customer_id']
    return Address.objects.create(customer_id=customer,**self.validated_data)
  
  
class CustomerSerializer(serializers.ModelSerializer):
  user_id = serializers.IntegerField(read_only=True)
  address = AddressSerializer(read_only=True)
  class Meta:
    model = Customer
    fields = ['id','birth_date','phone','membership','user_id','address']

  
class OrderItemSerializer(serializers.ModelSerializer):
  product = SimpleProductSerializer()
  class Meta:  
    model = OrderItem
    fields = ['id','product','unit_price','quantity']
    
    
class OrderSerializer(serializers.ModelSerializer):
  items = OrderItemSerializer(many=True)
  class Meta:
    model = Order
    fields = ['id','customer','placed_at','payment_status','items']
  
  
class CreateOrderSerializer(serializers.Serializer):
  cart_id = serializers.UUIDField()
  
  def validate_cart_id(self,cart_id):
    if not Cart.objects.filter(id=cart_id).exists():
      raise serializers.ValidationError('Cart Does Not Exist')
    elif CartItem.objects.filter(cart_id=cart_id).count() == 0 :
      raise serializers.ValidationError('Empty Cart')
    return cart_id
  
  def save(self, **kwargs):
    with transaction.atomic():
      cart_id = self.validated_data['cart_id']
      user_id = self.context['user_id']
      customer = Customer.objects.get(user_id=user_id)
      cart_items = CartItem.objects.filter(cart_id=cart_id)
      order = Order.objects.create(customer = customer)
      
      order_items = [OrderItem(
        order = order,
        product = item.product,
        unit_price = item.product.unit_price,
        quantity = item.quantity
        ) for item in cart_items]
      
      OrderItem.objects.bulk_create(order_items)
      Cart.objects.filter(pk=cart_id).delete() 
      if 'cart_session' in self.context:
        del self.context['cart_session']
      return order
  

class UpdateOrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order
    fields = ['payment_status']
    


    
  