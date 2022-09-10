from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import UserForm,ClientForm
from .models import Medicament,Category,Subcategory,Subcategorye,Client,Commande,CommandeItem
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required # Create your views here.
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import SimpleTestCase, override_settings
from .utils import remove_filter
from django.http import JsonResponse
import json
import smtplib
from email.message import EmailMessage
from django.conf import settings
from datetime import datetime
from django.contrib import messages 

# index home page
class home(ListView):
    template_name = "store/index-2.html"
    context_object_name = "lists"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cats"] = Category.objects.all()
        context["news"] = Medicament.objects.order_by("-date")[:10]
        context["solded"] = Medicament.objects.all()
        context["creme"] = Medicament.objects.get(name="DUCRAY MELASCREEN ECLAT CREME RICHE SPF15, 40ML")
        nbhomme=0
        nbvisage =0
        nbsolaire =0
        nbcorps =0
        for items in Category.objects.get(name="Homme").subcategory.all():
            for item in items.subcategorye.all():
                nbhomme+=item.medicament_set.all().count()
        context["nbhomme"] = nbhomme 
        for items in Category.objects.get(name="Corps").subcategory.all():
            for item in items.subcategorye.all():
                nbcorps+=item.medicament_set.all().count()
        context["nbcorps"] = nbcorps 
        for items in Category.objects.get(name="Solaire").subcategory.all():
            for item in items.subcategorye.all():
                nbsolaire+=item.medicament_set.all().count()
        context["nbsolaire"] = nbsolaire 
        for items in Category.objects.get(name="Visage").subcategory.all():
            for item in items.subcategorye.all():
                nbvisage+=item.medicament_set.all().count()
        context["nbvisage"] = nbvisage 
        cart={}
        if self.request.user.is_authenticated:
            try:
                context["objects"] = Commande.objects.get(client=self.request.user.client).items.all()
                nb_items = Commande.objects.get(client=self.request.user.client).items.all().count()
                context["nb_items"] = nb_items
                context["totale"] = Commande.objects.get(client=self.request.user.client).totale()
                context["totales"] = float(context["totale"]) + 7 
                
            except:
                context["objects"] = Commande.objects.none()
                context["nb_items"] = 0
        else:
            try:
                cart = json.loads(self.request.COOKIES['cart'])
            except:
                cart={}
            nb_items = 0
            items = []
            order = {"totale":0,"nb_items":0}
            for i in cart:
                nb_items+=cart[i]['quantite']
                product = Medicament.objects.get(id=i)
                if product.solde:
                    total = product.solding() * cart[i]['quantite']
                else:
                    total = product.prix * cart[i]['quantite']
                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'image':product.image,
                        'prix':product.prix,
                        'description':product.description,
                        'solde':product.solde,
                        'subcategorye':product.subcategorye,
                        'slug':product.slug,
                        "solding":product.solding()
                    },
                    'quantite':cart[i]['quantite'],
                    'get_items_price':total
                }
                items.append(item)
                
                order["nb_items"] += cart[i]['quantite']
                order["totale"] += total
            context["nb_items"] = order["nb_items"]
            context["totale"] = order["totale"]
            context["objects"] = items
        return context

    def get_queryset(self):
        queryset = Medicament.objects.order_by("-date").distinct()
        
        return queryset 
    

class MedicamentListView(ListView):
    context_object_name = "lists"
    template_name = "store/shop-grid-sidebar-left.html"
    paginate_by = 12
    queryset = Medicament.objects.order_by("-date").distinct()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list"] = Medicament.objects.all().order_by("-date")[:3]
        context["obj"] = Medicament.objects.get(id=20)
        context["cats"] = Category.objects.all()
        search = self.request.GET.get('search')
        if search:
            sub = Subcategorye.objects.filter(name__iexact=search).first()
            print("hello 1")
            if sub:
                cat = sub.subcategory_set.first()
                try:
                    context["similaire_cats"] = cat.subcategorye.all()
                except:
                    context["similaire_cats"] = None
        if self.request.user.is_authenticated:
            try:
                context["objects"] = Commande.objects.get(client=self.request.user.client).items.all()
                nb_items = Commande.objects.get(client=self.request.user.client).items.all().count()
                context["nb_items"] = nb_items
                context["totale"] = Commande.objects.get(client=self.request.user.client).totale()
                context["totales"] = float(context["totale"]) + 7 

            except:
                context["objects"] = Commande.objects.none()
                context["nb_items"] = 0
        else:
            try:
                cart = json.loads(self.request.COOKIES['cart'])
            except:
                cart={}
            nb_items = 0
            items = []
            order = {"totale":0,"nb_items":0}
            for i in cart:
                nb_items+=cart[i]['quantite']
                product = Medicament.objects.get(id=i)
                if product.solde:
                    total = product.solding() * cart[i]['quantite']
                else:
                    total = product.prix * cart[i]['quantite']
                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'image':product.image,
                        'prix':product.prix,
                        'description':product.description,
                        'solde':product.solde,
                        'subcategorye':product.subcategorye,
                        'slug':product.slug,
                        "solding":product.solding()
                    },
                    'quantite':cart[i]['quantite'],
                    'get_items_price':total
                }
                items.append(item)
                
                order["nb_items"] += cart[i]['quantite']
                order["totale"] += total
            context["nb_items"] = order["nb_items"]
            context["totale"] = order["totale"]
            context["objects"] = items
        return context

    def get_queryset(self):
        queryset = Medicament.objects.order_by("-date").distinct()
        search = self.request.GET.get('search')
        if search:
            sub = Subcategorye.objects.filter(name__iexact=search).first()
            if sub is None:
                qs = Medicament.objects.filter(name__icontains=search)
                if qs:
                    return qs
                return Subcategorye.objects.none()
            q1 = sub.medicament_set.all().order_by("-date")
            return q1
        return queryset

class MedicamentDetailView(DetailView):
    model = Medicament
    template_name = "store/product-details-default.html"
    context_object_name = 'obj'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart={}
        
        if self.request.user.is_authenticated:
            try:
                context["objects"] = Commande.objects.get(client=self.request.user.client).items.all()
                nb_items = Commande.objects.get(client=self.request.user.client).items.all().count()
                context["nb_items"] = nb_items
                context["totale"] = Commande.objects.get(client=self.request.user.client).totale()
                context["totales"] = float(context["totale"]) + 7 
                
            except:
                context["objects"] = Commande.objects.none()
                context["nb_items"] = 0
        else:
            try:
                cart = json.loads(self.request.COOKIES['cart'])
            except:
                cart={}
            nb_items = 0
            items = []
            order = {"totale":0,"nb_items":0}
            for i in cart:
                nb_items+=cart[i]['quantite']
                product = Medicament.objects.get(id=i)
                if product.solde:
                    total = product.solding() * cart[i]['quantite']
                else:
                    total = product.prix * cart[i]['quantite']
                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'image':product.image,
                        'prix':product.prix,
                        'description':product.description,
                        'solde':product.solde,
                        'subcategorye':product.subcategorye,
                        'slug':product.slug,
                        "solding":product.solding()
                    },
                    'quantite':cart[i]['quantite'],
                    'get_items_price':total
                }
                items.append(item)
                
                order["nb_items"] += cart[i]['quantite']
                order["totale"] += total
            context["nb_items"] = order["nb_items"]
            context["totale"] = order["totale"]
            context["objects"] = items
        context["similaire"] = Medicament.objects.filter(subcategorye = self.object.subcategorye)
        return context
    
    
class MedicamentCreateView(CreateView):
    model = Medicament
    template_name = "create-medicament-admib.html"
    fields = ("name","prix","image","description","quantite","solde","subcategorye")
    template_name = "store/create-medicament-admin.html"
    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'slug': self.object.slug})
class MedicamentUpdateView(UpdateView):
    model = Medicament
    template_name = "store/update-medicament-admin.html"
    fields = ("name","prix","image","description","quantite","solde","subcategorye")
    context_object_name = 'obj'
    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'slug': self.object.slug})
class MedicamentDeleteView(DeleteView):
    model = Medicament
    template_name = "store/delete-medicament-admin.html"
    success_url = "/"

class MainListView(ListView):
    model = Medicament
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cats"] = Category.objects.all().distinct()
        context["objects"] =  Commande.objects.get(client=self.request.user.client)
        return context

class UserCreateView(CreateView):
    form_class = UserForm
    template_name = "registration/user-register.html"
    success_url = reverse_lazy("login")


def ClientCreateView(request):
    instance = ClientForm()
    form = ClientForm()
    context = {}
    cart={}
    
    if request.method == "POST":
        if request.user.is_authenticated:
         if  request.user.client:
            client = Client.objects.get(user=request.user)
            instance = ClientForm(request.POST or None, instance = client)
            if instance.is_valid():
                instance.save()
                # succ message
                #sending email after saving the commande
                subject = 'Parapharmacy'
                admin_subject = "Nouveau Commande : " + str(datetime.now())
                message = f'Hi {request.user.username}, Merci pour votre confiance ,votre commande est passé par succés pour plus d"information appeller le {settings.MY_PHONE_NUMBER}'
                admin_message = f'Commande passe par {request.user.username} qui habite a {request.user.client.adresse} et qui payer {str(float(Commande.objects.get(client=client).totale()+7))}DT pour les produit {str(Commande.objects.get(client=client).items.all())}'
                #admin_message = f'Commande passe par {request.user.username} qui habite a {request.user.client.adresse} et qui payer {str(Commande.objects.get(client=client).totale())}DT pour les produit {str(Commande.objects.get(client=client).items.all())}'
                smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
                smtpserver.ehlo()
                smtpserver.starttls()
                smtpserver.ehlo()
                smtpserver.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                msg = EmailMessage()
                admin_msg = EmailMessage()
                msg.set_content(message)
                admin_msg.set_content(admin_message)
                msg['Subject']= subject
                admin_msg['Subject'] = admin_subject
                try:
                    smtpserver.sendmail(settings.EMAIL_HOST_USER,request.user.client.email,msg.as_string())
                    smtpserver.sendmail(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_USER,admin_msg.as_string())
                except:
                    print('An error occurred when trying to send an email')
                    messages.error(request, "Try again! Order Failed!")

                smtpserver.quit()

                Commande.objects.get(client=client).delete()
            
                messages.success(request,"votre commande est passe par succee") 
                return redirect("index")

    if request.user.is_authenticated:
        try:
            context["objects"] = Commande.objects.get(client=request.user.client).items.all()
            nb_items = Commande.objects.get(client=request.user.client).items.all().count()
            context["nb_items"] = nb_items
            context["totale"] = Commande.objects.get(client=request.user.client).totale()
            context["totales"] = float(context["totale"]) + 7 
            
        except:
                context["objects"] = Commande.objects.none()
                context["nb_items"] = 0

    # geust user
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart={}

        nb_items = 0
        items = []
        order = {"totale":0,"nb_items":0}
        for i in cart:
            nb_items+=cart[i]['quantite']
            product = Medicament.objects.get(id=i)
            if product.solde:
                total = product.solding() * cart[i]['quantite']
            else:
                total = product.prix * cart[i]['quantite']
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'image':product.image,
                    'prix':product.prix,
                    'description':product.description,
                    'solde':product.solde,
                    'subcategorye':product.subcategorye,
                    'slug':product.slug,
                    "solding":product.solding()
                },
                'quantite':cart[i]['quantite'],
                'get_items_price':total
            }
            items.append(item)
            
            order["nb_items"] += cart[i]['quantite']
            order["totale"] += total
        context["nb_items"] = order["nb_items"]
        context["totale"] = order["totale"]
        context["totales"] = float(order["totale"]) + 7 
        context["objects"] = items
    context["form"] = instance
    if request.POST:
        client = ClientForm(request.POST or None)
        if client.is_valid():
            client.save()
            #sending email after saving the commande
            subject = 'Parapharmacy'
            admin_subject = "Nouveau Commande : " + str(datetime.now())
            message = f'Hi {request.POST["username"]}, Merci pour votre confiance ,votre commande est passé par succés.pour plus information appeller le {settings.MY_PHONE_NUMBER}'
            admin_message = f'Commande passe par {request.POST["username"]} qui habite a {request.POST["adresse"]} et qui payer {context["totale"]}DT pour plus information {request.POST["phone"]}' 
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            msg = EmailMessage()
            admin_msg = EmailMessage()
            msg.set_content(message)
            admin_msg.set_content(admin_message)
            msg['Subject']= subject
            admin_msg['Subject'] = admin_subject
            try:
                smtpserver.sendmail(settings.EMAIL_HOST_USER,request.POST["email"],msg.as_string())
                smtpserver.sendmail(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_USER,admin_msg.as_string())
            except:
                pass
            smtpserver.quit()
            response = redirect("index")
            response.delete_cookie('cart')
            return response
    return render(request, "store/checkout.html",context)

def update_item(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    # print('Product id: ' + product_id)
    # print('Action: ' + action)
    if request.user.is_authenticated:
        client = request.user.client
    product = Medicament.objects.get(id=product_id)
    order,created = Commande.objects.get_or_create(client=client,complete=False)
    item,created = CommandeItem.objects.get_or_create(product=product)
    order.items.add(item)
    if action == 'add':
        item.quantite = int(item.quantite + 1)
        messages.success(request, "medicament est ajoute au panier")
    elif action == 'delete' and item.quantite > 0:
        # if item.quantite == 0:
        #     item.delete()
        #     return
        item.quantite = int(item.quantite - 1)
        messages.warning(request, "medicament est supprimer au panier")
    elif action == 'remove':
        messages.error(request, "medicament est supprimer completement!")
        item.quantite = 0
        item.delete()
    else:
        item.favorable_by = int(item.favorable_by + 1)
    item.save()
    if item.quantite <= 0:
        item.delete()
    return JsonResponse("item was added",safe=False)




    # sending email logique
      #send email after renew                
                # subject = 'welcome to Belha world'
                # message = f'Hi {request.user.username}, thank you for ur confidence to us :)'
                # # email_from = settings.EMAIL_HOST_USER
                # print(request.user.email)
                # print(settings.EMAIL_HOST_USER)
                # # recipient_list = [request.user.email, ]
                # # send_mail( subject, message, email_from, recipient_list )

                # server = smtplib.SMTP('smtp.gmail.com', 587)
                # server.starttls()
                # server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                # msg = EmailMessage()
                # msg.set_content(message)
                # msg['Subject']= subject
                # try:
                #     server.sendmail(settings.EMAIL_HOST_USER,request.user.email,msg.as_string())
                # except:
                #     print('An error occurred when trying to send an email')

                # server.quit()


# class CheckoutCreateView(ListView):
#     template_name = "store/checkout.html"
#     queryset = Commande.objects.none()
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.user.is_authenticated:
#             try:
#                 context["objects"] = Commande.objects.get(client=self.request.user.client).items.all()
#                 nb_items = Commande.objects.get(client=self.request.user.client).items.all().count()
#                 context["nb_items"] = nb_items
#                 context["totale"] = Commande.objects.get(client=self.request.user.client).totale()
#             except:
#                 context["objects"] = Commande.objects.none()
#                 context["nb_items"] = 0
#         else:
#             try:
#                 cart = json.loads(self.request.COOKIES['cart'])
#             except:
#                 cart={}
#             nb_items = 0
#             items = []
#             order = {"totale":0,"nb_items":0}
#             for i in cart:
#                 nb_items+=cart[i]['quantite']
#                 product = Medicament.objects.get(id=i)
#                 totale = product.prix * cart[i]['quantite']

#                 order["nb_items"] += cart[i]['quantite']
#                 order["totale"] += totale
#             context["nb_items"] = order["nb_items"]
#             context["totale"] = order["totale"]
#             context["objects"] = items
#         return context
    

class CartListView(ListView):
    template_name = "store/cart.html"
    queryset = Commande.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = {}
        if self.request.user.is_authenticated:
            try:
                context["objects"] = Commande.objects.get(client=self.request.user.client).items.all()
                nb_items = Commande.objects.get(client=self.request.user.client).items.all().count()
                context["nb_items"] = nb_items
                context["totale"] = Commande.objects.get(client=self.request.user.client).totale()
                context["totales"] = float(context["totale"]) + 7 
            except:
                context["objects"] = Commande.objects.none()
                context["nb_items"] = 0
        else:
            try:
                cart = json.loads(self.request.COOKIES['cart'])
            except:
                cart={}
            nb_items = 0
            items = []
            order = {"totale":0,"nb_items":0}
            for i in cart:
                nb_items+=cart[i]['quantite']
                product = Medicament.objects.get(id=i)
                if product.solde:
                    total = product.solding() * cart[i]['quantite']
                else:
                    total = product.prix * cart[i]['quantite']
                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'image':product.image,
                        'prix':product.prix,
                        'description':product.description,
                        'solde':product.solde,
                        'subcategorye':product.subcategorye,
                        'slug':product.slug,
                        "solding":product.solding()
                    },
                    'quantite':cart[i]['quantite'],
                    'get_items_price':total
                }
                items.append(item)
                
                order["nb_items"] += cart[i]['quantite']
                order["totale"] += total
            context["nb_items"] = order["nb_items"]
            context["totale"] = order["totale"]
            context["objects"] = items
            context["totales"] = float(order["totale"]) + 7 
            context["objects"] = items
        return context
    
