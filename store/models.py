from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .validators import validate_length
from .utils import unique_slug_generator
from datetime import datetime
# Create your models here.

class Subcategorye(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    subcategorye = models.ManyToManyField(Subcategorye,blank=True)
    def __str__(self):
        return self.name
    
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    subcategory = models.ManyToManyField(Subcategory,blank=True)
    image = models.ImageField(upload_to="navbar",null=True,blank=True)
    def __str__(self):
        return self.name
    
class Medicament(models.Model):
    name = models.CharField(max_length=200)
    quantite = models.IntegerField(default=100)
    subcategorye = models.ForeignKey(Subcategorye, on_delete=models.CASCADE,null=True,blank=True)
    description = models.TextField(blank=True,null=True)
    prix = models.DecimalField(max_digits=8,decimal_places=3)
    solde = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
    image = models.ImageField(upload_to="medicament-images/%y/%m",null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True,blank=True)
    def __str__(self):
        return self.name
    # def save(self,*args, **kwargs):
    #     super(Medicament, self).save(*args, **kwargs)
    def solding(self):
        prix1=0
        if self.solde:
            prix1 = (self.prix * (1 - (self.solde/100) ))
        return prix1
    
class Client(models.Model):
    sexe_choice = (("homme","homme"),
                ("femme","femme"))
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    adresse = models.CharField(max_length=200,default="Arianna")
    email = models.EmailField(blank=True,null=True)
    phone = models.CharField(validators=[validate_length,],max_length=8,default="23601888")
    username = models.CharField(max_length=50,null=True,blank=True)
    lastname = models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
        return str(self.pk)
    
    
class CommandeItem(models.Model):
    product = models.OneToOneField(Medicament, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(null=True,blank=True,default=0)
    # commande = models.ForeignKey(Commande, on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    favorable_by = models.PositiveIntegerField(null=True,blank=True,default=0)
    def get_items_price(self):
        return self.product.prix * self.quantite
    def __str__(self):
        return self.product.name
    
class Commande(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL,null=True)
    complete = models.BooleanField(default=False)
    items = models.ManyToManyField(CommandeItem)
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        return str(self.pk)
    def totale(self):
        s = 0
        for item in self.items.all():
            s = s + float(item.get_items_price())
        return s
class Marque(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="navbar/marque") 
    def __str__(self):
        return self.name
    

@receiver(pre_save, sender=Medicament)
def pre_save_receiver(sender, instance, *args, **kwargs):
   if not instance.slug:
       instance.slug = unique_slug_generator(instance)
