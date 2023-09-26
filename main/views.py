from django.shortcuts import redirect, render
from main.models import  Componente, Perfil
from main.forms import UsuarioForm
from main.Carrito import Carrito
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
import requests
import json

def index(request):
    componentes = Componente.objects.all()
    return render(request, 'main/index.html', {'componentes':componentes}) 

class ComponenteList(ListView):
    model = Componente
    context_object_name = "componentes"

class ComponenteMineList(LoginRequiredMixin, ComponenteList):
    
    def get_queryset(self):
        return Componente.objects.filter(publisher=self.request.user.id).all()


class ComponenteDetail(DetailView):
    model = Componente
    context_object_name = "componente"


class ComponenteUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Componente
    success_url = reverse_lazy("componente-list")
    fields = '__all__'

    def test_func(self):
        user_id = self.request.user.id
        Componente_id =  self.kwargs.get("pk")
        return Componente.objects.filter(publisher=user_id, id=Componente_id).exists()


class ComponenteDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Componente
    context_object_name = "Componentes"
    success_url = reverse_lazy("componente-list")

    def test_func(self):
        user_id = self.request.user.id
        Componente_id =  self.kwargs.get("pk")
        return Componente.objects.filter(id=Componente_id).exists()


class ComponenteCreate(LoginRequiredMixin, CreateView):
    model = Componente
    success_url = reverse_lazy("componente-list")
    fields = '__all__'


class ComponenteSearch(ListView):
    model = Componente
    context_object_name = "componentes"

    def get_queryset(self):
        criterio = self.request.GET.get("criterio")
        result = Componente.objects.filter(producto__icontains=criterio).all()
        return result

class Login(LoginView):
    next_page = reverse_lazy("index")


class SignUp(CreateView):
    form_class = UsuarioForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('componente-list')


class Logout(LogoutView):
    template_name = "registration/logout.html"


class PerfilCreate(LoginRequiredMixin, CreateView):
    model = Perfil
    success_url = reverse_lazy("index")
    fields = ['domicilio', 'altura', 'localidad', 'codigoPostal', 'numero', 'mail']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PerfilUpdate(LoginRequiredMixin, UserPassesTestMixin,  UpdateView):
    model = Perfil
    success_url = reverse_lazy("componente-list")
    fields = ['domicilio', 'altura', 'localidad', 'codigoPostal', 'numero', 'mail']

    def test_func(self):
        return Perfil.objects.filter(user=self.request.user).exists()
    

def Carro(request):
    return render(request, 'main/carrito.html')

def agregar_componente(request, componente_id):
    carrito = Carrito(request)
    componente = Componente.objects.get(id=componente_id)
    carrito.agregar(componente)
    return redirect("carro")

def eliminar_componente(request, componente_id):
    carrito = Carrito(request)
    componente = Componente.objects.get(id=componente_id)
    carrito.eliminar_carrito(componente)
    return redirect("carro")

def restar_componente(request, componente_id):
    carrito = Carrito(request)
    componente = Componente.objects.get(id=componente_id)
    carrito.restar(componente)
    return redirect("carro")

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("carro")


client_id = 'TEST-3c61abc0-33d7-477b-a92f-7932cd05fb78'
client_secret = 'TEST-839647108512701-092615-2b79ab3fdec2c37df347dc7bcadaf29b-265252285'

def obtener_token():
    url = 'https://api.mercadopago.com/oauth/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, data=data)
    token_data = response.json()
    return token_data['access_token']

def crear_pago(access_token):
    url = 'https://api.mercadopago.com/checkout/preferences'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'items': [
            {
                'title': 'Producto de prueba',
                'quantity': 1,
                'currency_id': 'ARS',
                'unit_price': 100.00
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    pago_data = response.json()
    return pago_data

def iniciar_pago(request):
    access_token = obtener_token()
    pago = crear_pago(access_token)
    return render(request, 'pago.html', {'redirect_url': pago['init_point']})