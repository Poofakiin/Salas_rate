"""
URL configuration for ReseñasSalasBeauchef project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.sign_up, name = 'register'),
    path('login/', views.sign_in, name='login'),
    path('', views.index, name="index"),
    path('todas-las-salas/', views.todas_las_salas, name='todas-las-salas'),
    path('hacer-reseña/', views.hacer_resena, name='hacer-reseña'),
    path('salas-por-edificio/', views.salas_por_edificio, name='salas-por-edificio'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre-nosotros'),
    path('novedades/', views.novedades, name='novedades'),
    path('logout/', views.logout_view, name='logout'),
    path('salas/<int:id_sala>/', views.pagResenas, name='pagResenas'),
    path('buscador-salas/', views.buscador_salas, name='buscador-salas'),
    path('crear-anuncio/', views.crear_anuncio, name='crear-anuncio'),
    path('ver-anuncios/', views.ver_anuncios, name='ver-anuncios'),
    path('save-comment/', views.save_comment, name='save-comment'),
    path('like/', views.LikeView, name='like_review'),
    path('likecomment/', views.LikeComment, name='like_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)