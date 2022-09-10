from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.defaults import page_not_found
from django.conf.urls import (
handler400, handler403, handler404, handler500
)
urlpatterns = [
    path('store/',views.MedicamentListView.as_view(),name="store"),
    path('update_item/',views.update_item,name="update_item"),
    path('checkout/',views.ClientCreateView,name="checkout"),
    path('cart/',views.CartListView.as_view(),name="cart"),
    path('accounts/register/',views.UserCreateView.as_view(),name="register"),
    path('<slug:slug>/delete/',views.MedicamentDeleteView.as_view(),name="delete"),
    path('<slug:slug>/update/',views.MedicamentUpdateView.as_view(),name="update"),
    path('create/',views.MedicamentCreateView.as_view(),name="create"),
    path('<slug:slug>/',views.MedicamentDetailView.as_view(),name="detail"),
    path('',views.home.as_view(),name="index"),
    path('main/',views.MainListView.as_view(),name="main"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
