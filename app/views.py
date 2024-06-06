from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import *

# Create your views here.

def index(request):
    return render(request, 'app/index.html')

def registro(request): 
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirige a la página de inicio después del registro
    else:
        form = RegisterForm()
    return render(request,'registration/registro.html', {'form': form})

def orden(request):
    if request.method == 'POST':
        nombre_cliente = request.POST.get('nombreCliente')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        codigo_postal = request.POST.get('codigoPostal')

        nueva_orden = Orden.objects.create(
            empresa=nombre_cliente,
            direccion=direccion,
            telefono=telefono,
            correo=correo,
            codigo_postal=int(codigo_postal)
        )

        # Redirigir a la página de factura, pasando el id de la orden recién creada
        return redirect('factura', orden_id=nueva_orden.id_orden)

    return render(request, 'app/orden.html')

def factura(request):
    return render(request, 'app/factura.html')

