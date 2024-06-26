from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from .forms import *
from .models import *

# Create your views here.

def index(request):
    facturas = Factura.objects.all()
    
    # Pasar las facturas al contexto del renderizado del template
    return render(request, 'app/index.html', {'facturas': facturas})

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

@login_required
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

@login_required
def factura(request, orden_id):
    if request.method == 'POST':
        # Obtener la orden
        orden = Orden.objects.get(id_orden=orden_id)
        
        # Procesar los datos del formulario de factura
        productos = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio')
        subtotales = request.POST.getlist('total')

        # Convertir los subtotales a enteros y filtrar los valores no válidos o cadenas vacías
        subtotales = [subtotal.strip() for subtotal in subtotales if subtotal.strip()]
        subtotal = round(sum(int(subtotal) for subtotal in subtotales), 2)
        iva = round(subtotal * 0.19, 2)
        total = round(subtotal + iva, 2)

        # Obtener el estado 'Procesando' desde la base de datos
        estado_procesando = Estado.objects.get(estado='Procesando')

        # Crear la nueva factura
        nueva_factura = Factura.objects.create(
            orden=orden,
            estado=estado_procesando,
            subtotal=subtotal,
            iva=iva,
            total=total
        )

        # Crear los productos asociados a la factura
        for producto, cantidad, precio, subtotal in zip(productos, cantidades, precios, subtotales):
            if subtotal.strip():  # Verifica si subtotal no está vacío
                ProductoFactura.objects.create(
                    factura=nueva_factura,
                    producto=producto,
                    cantidad=int(cantidad),
                    precio_unitario=int(precio),
                    precio_total=int(subtotal)
                )

        # Redirigir a la página de inicio (index)
        return redirect('index')
    else:
        # Si no es una solicitud POST, obtener los datos de la orden y renderizar la plantilla de factura
        orden = Orden.objects.get(id_orden=orden_id)
        return render(request, 'app/factura.html', {'orden': orden})