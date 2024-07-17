from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from xhtml2pdf import pisa
from bs4 import BeautifulSoup
from django.template.loader import get_template
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfWriter, PdfReader
from .forms import *
from .models import *

# Create your views here.

def index(request):
    query = request.GET.get('q')
    if query:
        facturas = Factura.objects.filter(id_factura__icontains=query)
    else:
        facturas = Factura.objects.all()
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
        nombre_vendedor = request.POST.get('nombreVendedor')
        rut_vendedor = request.POST.get('rutVendedor')
        telefono_vendedor = request.POST.get('telefonoVendedor')
        correo_vendedor = request.POST.get('correoVendedor')

        nueva_orden = Orden.objects.create(
            empresa=nombre_cliente,
            direccion=direccion,
            telefono=telefono,
            correo=correo,
            codigo_postal=int(codigo_postal),
            vendedor=nombre_vendedor,
            rut_vendedor=rut_vendedor,
            telefono_vendedor=telefono_vendedor,
            correo_vendedor=correo_vendedor
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

        # Obtener el estado 'Creada' y 'Por entregar' desde la base de datos
        estado_fact = Estado.objects.get(estado='Creada')
        estado_entrega = EstadoEntrega.objects.get(estado_entrega='Por entregar')

        # Crear la nueva factura
        nueva_factura = Factura.objects.create(
            orden=orden,
            estado=estado_fact,
            estado_entrega=estado_entrega,
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
        return redirect('detalle_factura', id_factura=nueva_factura.id_factura)
    else:
        # Si no es una solicitud POST, obtener los datos de la orden y renderizar la plantilla de factura
        orden = Orden.objects.get(id_orden=orden_id)
        return render(request, 'app/factura.html', {'orden': orden})

def render_to_pdf(html):
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
    if not pdf.err:
        return result.getvalue()
    return None

def add_watermark(input_pdf, watermark_text):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 100)
    can.setFillColorRGB(255.9, 0.9, 0.9, alpha=0.8)  # Light gray color
    can.saveState()
    can.translate(300, 500)
    can.rotate(45)
    can.drawCentredString(0, 0, watermark_text)
    can.restoreState()
    can.save()

    packet.seek(0)
    watermark = PdfReader(packet)
    existing_pdf = PdfReader(BytesIO(input_pdf))
    output = PdfWriter()

    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[i]
        page.merge_page(watermark.pages[0])
        output.add_page(page)

    output_stream = BytesIO()
    output.write(output_stream)
    return output_stream.getvalue()

@login_required    
def detalle_factura(request, id_factura):
    factura = get_object_or_404(Factura, id_factura=id_factura)
    productos = ProductoFactura.objects.filter(factura=factura)
    rechazos = HistorialRechazo.objects.filter(factura=id_factura)
    aceptacion = Aceptacion.objects.filter(factura=id_factura)

    datos = {
        'listaFactura': [factura],
        'productos': productos,
        'rechazos': rechazos,
        'aceptacion': aceptacion
    }

    estado_fact = Estado.objects.get(estado='Anulada')
    if request.method == 'POST':
        factura.estado = estado_fact
        factura.save()
        return redirect('detalle_factura', id_factura=id_factura)

    if request.GET.get('download') == 'pdf':
        template = get_template('app/detalle_factura.html')
        html = template.render(datos)

        # Usar BeautifulSoup para extraer solo el contenido deseado
        soup = BeautifulSoup(html, 'html.parser')
        pdf_content = soup.find(class_='pdf-content')
        html = str(pdf_content) if pdf_content else html  # Convertir de nuevo a string

        pdf = render_to_pdf(html)
        if pdf:
            if factura.estado.estado == 'Anulada':
                pdf = add_watermark(pdf, "ANULADA")

            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="detalle_factura_{id_factura}.pdf"'
            return response

        return HttpResponse('Tuvimos algunos errores <pre>' + html + '</pre>')

    return render(request, 'app/detalle_factura.html', datos)

def modificar(request, id_factura):
    estados_entrega = EstadoEntrega.objects.all()
    if id_factura:
        factura = get_object_or_404(Factura, id_factura=id_factura)
        orden = factura.orden
        productos = ProductoFactura.objects.filter(factura=factura)
    else:
        factura = None
        orden = None
        productos = []

    datos = {
        'listaFactura': factura,
        'listaOrden': [orden] if orden else [],
        'productos': productos,
        'estados_entrega': estados_entrega
    }

    if request.method == 'POST':
        nombre_cliente = request.POST.get('nombreCliente')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        codigo_postal = request.POST.get('codigoPostal')

        if orden:
            orden.empresa = nombre_cliente
            orden.direccion = direccion
            orden.telefono = telefono
            orden.correo = correo
            orden.codigo_postal = int(codigo_postal)
            orden.save()

        productos = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio')
        subtotales = request.POST.getlist('total')

        subtotales = [subtotal.strip() for subtotal in subtotales if subtotal.strip()]
        subtotal = round(sum(int(subtotal) for subtotal in subtotales), 2)
        iva = round(subtotal * 0.19, 2)
        total = round(subtotal + iva, 2)

        estado_fact = Estado.objects.get(estado='Rectificada')
        estado_entrega_id = request.POST.get('estadoEntrega')
        estado_entrega = get_object_or_404(EstadoEntrega, id_estado_entrega=estado_entrega_id)

        if factura:
            factura.orden = orden
            factura.subtotal = subtotal
            factura.iva = iva
            factura.total = total
            factura.estado = estado_fact
            factura.estado_entrega = estado_entrega
            factura.save()
            ProductoFactura.objects.filter(factura=factura).delete()
        else:
            factura = Factura.objects.create(
                orden=orden,
                estado=estado_fact,
                estado_entrega=estado_entrega,
                subtotal=subtotal,
                iva=iva,
                total=total
            )

        for producto, cantidad, precio, subtotal in zip(productos, cantidades, precios, subtotales):
            if subtotal.strip():
                ProductoFactura.objects.create(
                    factura=factura,
                    producto=producto,
                    cantidad=int(cantidad),
                    precio_unitario=int(precio),
                    precio_total=int(subtotal)
                )
        if estado_entrega.estado_entrega == 'Rechazado':
            motivo_rechazo = request.POST.get('motivoRechazo')

            historial_rechazo = HistorialRechazo(
                factura=factura,
                descripcion=motivo_rechazo
            )
            historial_rechazo.save()


        if estado_entrega.estado_entrega == 'Entregado':
            direccion_acept = request.POST.get('direccionEntrega')
            rut_acept = request.POST.get('rutReceptor')
            imagen_receptor = request.FILES.get('imagenReceptor')

            aceptacion = Aceptacion(
                factura=factura,
                direccionAcept=direccion_acept,
                rutAcept=rut_acept,
            )

            if imagen_receptor:
                aceptacion.img = imagen_receptor

            aceptacion.save()

        return redirect('detalle_factura', id_factura=factura.id_factura)
    
    return render(request, 'app/modificar.html', datos)
