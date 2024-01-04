from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Customer
from django.conf import settings

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def customer_create_when_user_created(sender,**kwargs):
  if kwargs['created']:
    Customer.objects.create(user=kwargs['instance'])
    