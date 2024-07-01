from django import forms
from .models import Sala, Usuario
from .models import Anuncio
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms




class ReviewForm(forms.Form):
    salas = [(sala.id, sala.NombreSala, ) for sala in Sala.objects.all()]
    salas = sorted(salas, key=lambda x: x[1])
    salas.insert(0, ('', 'Seleccione una sala'))
    sala = forms.ChoiceField(choices=salas)
    reseña = forms.CharField(widget=forms.Textarea(attrs={'class': 'non-resizable'}), max_length=400)

    
class BusquedaSalaForm(forms.Form):
    nombre_sala = forms.CharField(required=False)
    edificio = forms.ChoiceField(
        required=False,
        choices=[
             ('', ''),
            ('Beauchef 851', 'Beauchef 851'),
            ('Edificio Geología', 'Edificio Geología'),
            ('FCFM', 'FCFM'),
            ('Edificio Ingeniería Industrial', 'Edificio Ingeniería Industrial'),
            ('Edificio Central', 'Edificio Central'),
            ('Av. Blanco Encalada 2743', 'Av. Blanco Encalada 2743'),
            ('Edificio Civil', 'Edificio Civil'),
            ('Domeyko 2338 (DII)', 'Domeyko 2338 (DII)'),
            ('Edificio Escuela', 'Edificio Escuela'),
            ('Edificio Física', 'Edificio Física'),
            ('Edificio Eléctrica', 'Edificio Eléctrica'),
            ('Edificio Química', 'Edificio Química'),
            ('Edificio Computación', 'Edificio Computación'),
            # Agrega más opciones según sea necesario
        ],
    )
    capacidad_normal = forms.IntegerField(required=False)
    capacidad_examen = forms.IntegerField(required=False)
    aforo = forms.IntegerField(required=False)
    hibrido = forms.BooleanField(required=False, initial=False)
    promedio_visibilidad = forms.FloatField(required=False)
    promedio_sonido = forms.FloatField(required=False)
    promedio_asientos = forms.FloatField(required=False)
    promedio_iluminacion = forms.FloatField(required=False)
    calificacion_promedio_global = forms.FloatField(required=False)

class AnuncioForm(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ['sala', 'titulo', 'comentario', 'imagen']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address.', required=True)
    #userType = forms.
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'UserType', 'password1', 'password2']


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


