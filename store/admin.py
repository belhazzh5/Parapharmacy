from django.contrib import admin
from .models import Medicament,Category,Subcategorye,Subcategory,Client,Commande,CommandeItem,Marque
# Register your models here.
admin.site.register(Medicament)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Subcategorye)
admin.site.register(Client)
admin.site.register(Commande)
admin.site.register(CommandeItem)
admin.site.register(Marque)