from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Client

def post_save_user_receiver(sender,instance,created,*args,**kwargs):
    if created:
	    client,is_created = Client.objects.get_or_create(user=instance,username=instance.username,email=instance.email)
post_save.connect(post_save_user_receiver,sender=User)