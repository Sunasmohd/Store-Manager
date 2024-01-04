from django.shortcuts import render

# Create your views here.

def home(request):
  api_infos = [
    {'name':'Auth'},
    {'name':'Products','gp':'/products/','gppd':'/products/{product_id}/'},
    {'name':'Reviews','gp':'/products/{product_id}/reviews/','gppd':'/products/{product_id}/reviews/{review_id}/'},
    {'name':'Images','gp':'/products/{product_id}/images/','gppd':'/products/{product_id}/images/{image_id}/'},
    {'name':'Collections','gp':'/collections/','gppd':'/collections/{collection_id}/'},
    {'name':'Carts','gp':'/carts/','gppd':'/carts/{cart_id}/'},
    {'name':'Cart Items','gp':'/carts/{cart_id}/items/','gppd':'/carts/{cart_id}/items/{item_id}/'},
    {'name':'Customers','gp':'/customers/','gppd':'/customers/{customer_id}/'},
    {'name':'Address','gp':'/customers/{customer_id}/address/','gppd':'/customers/{customer_id}/address/{customer_id}/'},
    {'name':'Orders','gp':'/orders/','gppd':'/orders/{order_id}/'},
  ]
  return render(request,'index.html',context={'api_infos':api_infos})