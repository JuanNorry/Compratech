"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.views import (index, ComponenteList, ComponenteMineList, ComponenteUpdate, 
                                 ComponenteDelete, ComponenteDetail, ComponenteCreate, ComponenteSearch,
                                 PerfilCreate, PerfilUpdate, Login, SignUp, Logout, Carro, 
                                 agregar_componente, eliminar_componente, limpiar_carrito, restar_componente,)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('componente/list', ComponenteList.as_view(), name="componente-list"),
    path('componente/list/mine', ComponenteMineList.as_view(), name="componente-mine"),
    path('componente/<pk>/update', ComponenteUpdate.as_view(), name="componente-update"),
    path('componente/<pk>/delete', ComponenteDelete.as_view(), name="componente-delete"),
    path('componente/<pk>/detail', ComponenteDetail.as_view(), name="componente-detail"),
    path('componente/create', ComponenteCreate.as_view(), name="componente-create"),
    path('componente/search', ComponenteSearch.as_view(), name="componente-search"),
    path('login/', Login.as_view(), name="login"),
    path('signup/', SignUp.as_view(), name="signup"),
    path('logout/', Logout.as_view(), name="logout"),
    path('perfil/create', PerfilCreate.as_view(), name="perfil-create"),
    path('perfil/<pk>/update', PerfilUpdate.as_view(), name="perfil-update"),
    path('carro', Carro, name="carro"),
    path('carrito/<int:componente_id>/agregar', agregar_componente, name="Add"),
    path('carrito/<int:componente_id>/eliminar', eliminar_componente, name="Del"),
    path('carrito/<int:componente_id>/restar', restar_componente, name="Sub"),
    path('carrito/limpiar', limpiar_carrito, name="CLS"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)