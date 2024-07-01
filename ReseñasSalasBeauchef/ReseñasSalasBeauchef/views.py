
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from ReseñasSalasBeauchef.forms import ReviewForm, BusquedaSalaForm, AnuncioForm, UserRegistrationForm,UserLoginForm
from ReseñasSalasBeauchef.models import Sala, Usuario, Review, Anuncio, Comentario
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from collections import defaultdict
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.urls import reverse_lazy, reverse


# from ReseñasSalasBeauchef.models import Sala
# import json

# with open('ReseñasSalasBeauchef/fixtures/salas.json') as file:
#     data = json.load(file)
#     for item in data:
#         Sala.objects.create(**item['fields'])





#Landing page
def index(request):
    return render(request, "index.html")


#Las siguientes views corresponden a las paginas de la navbar
def todas_las_salas(request):
    # Fetch all Sala objects from the database
    salas = Sala.objects.all()
    salas = sorted(salas, key=lambda x: x.NombreSala)

    salas_por_pagina = 15
    paginator = Paginator(salas, salas_por_pagina)

    page = request.GET.get('page')
    try:
        salas = paginator.page(page)
    except PageNotAnInteger:
        salas = paginator.page(1)
    except EmptyPage:
        salas = paginator.page(paginator.num_pages)
    
    return render(request, 'todas-las-salas.html', {'salas': salas})


def salas_por_edificio(request):
    # Fetch all Sala objects from the database
    all_salas = Sala.objects.all()
    # Group salas by Edificio
    grouped_salas = {}
    for sala in all_salas:
        edificio = sala.Edificio
        if edificio not in grouped_salas:
            grouped_salas[edificio] = []
        grouped_salas[edificio].append(sala)

    return render(request, 'salas-por-edificio.html', {'grouped_salas': grouped_salas})


#View que procesa la busqueda de salas con filtros
def filtros(form):
    salas = Sala.objects.all()
    if form.cleaned_data['nombre_sala']:
        salas = salas.filter(NombreSala__icontains=form.cleaned_data['nombre_sala'])
    if form.cleaned_data['edificio']:
        salas = salas.filter(Edificio__icontains=form.cleaned_data['edificio'])
    if form.cleaned_data['capacidad_normal']:
        salas = salas.filter(CapacidadNormal__gte=form.cleaned_data['capacidad_normal'])
    if form.cleaned_data['capacidad_examen']:
        salas = salas.filter(CapacidadExamen__gte=form.cleaned_data['capacidad_examen'])
    if form.cleaned_data['aforo']:
        salas = salas.filter(Aforo__gte=form.cleaned_data['aforo'])
    if form.cleaned_data['hibrido']:
        salas = salas.filter(Hibrido=True)
    if form.cleaned_data['promedio_visibilidad']:
        salas = salas.filter(PromedioVisibilidad__gte=form.cleaned_data['promedio_visibilidad'])
    if form.cleaned_data['promedio_sonido']:
        salas = salas.filter(PromedioSonido__gte=form.cleaned_data['promedio_sonido'])
    if form.cleaned_data['promedio_asientos']:
        salas = salas.filter(PromedioAsientos__gte=form.cleaned_data['promedio_asientos'])
    if form.cleaned_data['promedio_iluminacion']:
        salas = salas.filter(PromedioIluminacion__gte=form.cleaned_data['promedio_iluminacion'])
    if form.cleaned_data['calificacion_promedio_global']:
        salas = salas.filter(CalificacionPromedioGlobal__gte=form.cleaned_data['calificacion_promedio_global'])
    return salas


def buscador_salas(request):
    if request.method == 'GET':
        form = BusquedaSalaForm(request.GET)
        salas_por_pagina = 15
        if form.is_valid():
            salas = filtros(form)
            page = request.GET.get('page', 1)
            paginator = Paginator(salas, salas_por_pagina)

            try:
                salas_pagina = paginator.page(page)
            except PageNotAnInteger:
                salas_pagina = paginator.page(1)
            except EmptyPage:
                salas_pagina = paginator.page(paginator.num_pages)

            return render(request, 'buscador-salas.html', {'form': form, 'salas': salas_pagina})
    else:
        form = BusquedaSalaForm()
    return render(request, 'buscador-salas.html', {'form': form})


@login_required(login_url='/login/')
def crear_anuncio(request):
    if request.user.UserType != 'Moderador':
        messages.error(request, 'Solo moderadores pueden acceder a esta página.')
        error_message = 'Solo moderadores pueden acceder a esta página.'
        return render(request,'ver-anuncios.html',{'error_message': error_message})

    if request.method == 'POST':
        form = AnuncioForm(request.POST, request.FILES)
        if form.is_valid():
            anuncio = form.save(commit=False)
            anuncio.usuario = request.user
            anuncio.save()
            return redirect('ver-anuncios')
    else:
        form = AnuncioForm()
    return render(request, 'crear-anuncio.html', {'form': form})


def ver_anuncios(request):
    anuncios = Anuncio.objects.all().order_by('-fecha_publicacion')
    return render(request, 'ver-anuncios.html', {'anuncios': anuncios})


def sobre_nosotros(request):
    return render(request, 'sobre-nosotros.html')


def novedades(request):
    return render(request, 'novedades.html')


#Listado de reseñas de una sala
def pagResenas(request, id_sala):
    sala = Sala.objects.get(pk = id_sala)
    
    # Filter reviews based on Sala and retrieve associated comments
    reviews = Review.objects.filter(Sala=id_sala)
    numResenas = len(reviews)
    reviews_with_comments = []
    for review in reviews:
        comentarios = Comentario.objects.filter(Reseña=review)
        reviews_with_comments.append((review, comentarios))
        
    filters = {
      'nombre_sala': sala.NombreSala,
    }
    form = BusquedaSalaForm(filters)

    return render(request, 'pagResenas.html', {'sala': sala, 'numResenas': numResenas, 'resenas': reviews_with_comments, 'form': form})


#Formulario para dejar reseñas
@login_required
def hacer_resena(request):
    if request.method == "POST":
        #Falta validar datos del form
        data = request.POST
        nuevaReview = Review()
        nuevaReview.User = Usuario.objects.get(username = request.user)
        sala = Sala.objects.get(pk = data["sala"])
        nuevaReview.Sala = sala
        numResenas = Review.objects.filter(Sala = sala).count()
        nuevaReview.Visibilidad = int(data["vis-rate"])
        nuevaReview.Sonido = int(data["sonido-rate"])
        nuevaReview.Asientos = int(data["asientos-rate"])
        nuevaReview.Iluminacion = int(data["iluminacion-rate"])
        nuevaReview.Reseña = data["reseña"]
        nuevaReview.save()

        #Actualizacion de promedio de puntajes en sala
        sala.CalificacionPromedioGlobal = ((sala.CalificacionPromedioGlobal * numResenas) + nuevaReview.Promedio) / (numResenas + 1)
        sala.PromedioVisibilidad = ((sala.PromedioVisibilidad * numResenas) + nuevaReview.Visibilidad) / (numResenas + 1)
        sala.PromedioAsientos = ((sala.PromedioAsientos * numResenas) + nuevaReview.Asientos) / (numResenas + 1)
        sala.PromedioIluminacion = ((sala.PromedioIluminacion * numResenas) + nuevaReview.Iluminacion) / (numResenas + 1)
        sala.PromedioSonido = ((sala.PromedioSonido * numResenas) + nuevaReview.Sonido) / (numResenas + 1)
        sala.save()

        return redirect('index') 

    else:
        form = ReviewForm()
        return render(request, "hacer-reseña.html", {"form": form})


# Registro
def sign_up(request):
    if request.method == 'GET':
        form = UserRegistrationForm()
        return render(request,'users/register.html', {'form': form})
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            #Restringir asignacion moderador
            if user.UserType == 'Moderador' and not request.user.is_superuser:
                messages.error(request, 'Solo administradores pueden asignar el rol Moderador')
                error_message = 'Solo administradores pueden asignar el rol Moderador'
                return render(request,'users/register.html',{'form': form, 'error_message': error_message})

            user.save()
            messages.success(request, 'You have succesfully signed up!')
            login(request,user)
            return redirect('index')
        else:
            return render(request,'users/register.html', {'form': form})
        

#Login
def sign_in(request):
    if request.method == 'GET':
        form = UserLoginForm()
        return render(request, 'users/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request, user)
                messages.success(request,f'Hi {username.title()}!')
                return redirect('index')
        
        # form is not valid or user is not authenticated
        messages.error(request,f'Nombre de usuario o contraseña inválida')
        error_message = 'Nombre de usuario o contraseña inválida'
        return render(request,'users/login.html',{'form': form, 'error_message': error_message})


#Logout
def logout_view(request):
    logout(request)
    return redirect('index') 

#Fin de la navbar

#Url point to save comments
@csrf_exempt
def save_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            comment = data.get('comment')
            if (comment):
                comentario = Comentario()
                comentario.User = Usuario.objects.get(username = request.user)
                comentario.Reseña = Review.objects.get(pk = data.get('resenaid'))
                comentario.Comentario = comment
                comentario.save()
            return JsonResponse({'success': True, 'commentId': comentario.pk})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


#Url point to save review likes
@csrf_exempt
def LikeView(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = Usuario.objects.get(username = request.user)
            post = Review.objects.get(pk = data.get('reviewId'))
            post.likes.add(user)
            return JsonResponse({'success': True, 'likes': post.puntuacion, 'commentId': post.pk})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


#Url point to save comment likes
@csrf_exempt
def LikeComment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = Usuario.objects.get(username = request.user)
            post = Comentario.objects.get(pk = data.get('commentId'))
            post.likes.add(user)
            return JsonResponse({'success': True, 'likes': post.puntuacion, 'commentId': post.pk})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
