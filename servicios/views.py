from django.shortcuts import render


from django.http import HttpResponse
import csv

from prompt_toolkit import HTML
from .models import Anuncio, Asistencia, DiaServicio, visita

def informe_asistencia(request, dia_servicio_id):
    # Obtén el servicio del día específico
    dia_servicio = DiaServicio.objects.get(id=dia_servicio_id)

    # Obtén las asistencias de ese día
    asistencias = Asistencia.objects.filter(dia_servicio=dia_servicio)

    # Crea la respuesta HTTP para el archivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="informe_asistencia_{dia_servicio.fecha_servicio}.csv"'

    # Crea un escritor CSV
    writer = csv.writer(response)
    writer.writerow(['Miembro', 'Aseo', 'Servicio'])  # Encabezado del CSV

    # Escribe los datos de las asistencias
    for asistencia in asistencias:
        writer.writerow([asistencia.miembro.nombre, asistencia.aseo, asistencia.servicio])

    return response


def reporte_asistencia_html(request, dia_servicio_id):
    dia_servicio = DiaServicio.objects.get(id=dia_servicio_id)
    asistencias = Asistencia.objects.filter(dia_servicio=dia_servicio)

    # Renderiza la plantilla HTML con los datos
    return render(request, 'reportes/asistencia.html', {'asistencias': asistencias, 'dia_servicio': dia_servicio})

def reporte_asistencia_pdf(request, dia_servicio_id):
    # Obtener el servicio del día
    dia_servicio = DiaServicio.objects.get(id=dia_servicio_id)
    asistencias = Asistencia.objects.filter(dia_servicio=dia_servicio)

    # Renderiza la plantilla HTML con los datos
    html = render(request, 'reportes/asistencia.html', {'asistencias': asistencias, 'dia_servicio': dia_servicio})

    # Genera el PDF a partir del HTML
    pdf = HTML(string=html.content.decode('utf-8')).write_pdf()

    # Retorna el PDF como una respuesta HTTP
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_asistencia_{dia_servicio.fecha_servicio}.pdf"'
    
    return response

from .models import DiaServicio, Asistencia, Miembro, TipoDeServicio, Aportacion, Gasto, Producto

from django.shortcuts import render, get_object_or_404, redirect
from .models import DiaServicio, TipoDeServicio, Miembro
from .forms import DiaServicioForm  # Suponiendo que tienes un formulario para DiaServicio

# Vista para editar el Día de Servicio
def editar_dia_servicio(request, id):
    # Obtener el objeto Día de Servicio que se va a editar
    dia_servicio = get_object_or_404(DiaServicio, id=id)

    # Obtener las opciones de TipoDeServicio y Miembro para los campos select
    tipos_de_servicio = TipoDeServicio.objects.all()
    miembros = Miembro.objects.all()

    if request.method == 'POST':
        # Crear el formulario con los datos enviados
        form = DiaServicioForm(request.POST, instance=dia_servicio)
        
        if form.is_valid():
            # Guardar los cambios
            form.save()
            # Redirigir al usuario a una página de éxito o detalles del servicio editado
            return redirect('detalles_dia_servicio', id=dia_servicio.id)
    else:
        # Si no es POST, simplemente crear el formulario con los datos actuales
        form = DiaServicioForm(instance=dia_servicio)

    context = {
        'dia_servicio': dia_servicio,
        'form': form,
        'tipos_de_servicio': tipos_de_servicio,
        'miembros': miembros,
    }

    return render(request, 'editar_dia_servicio.html', context)


def generar_informe_dia_servicio(request, dia_servicio_id):
    # Obtener el objeto DiaServicio por su ID
    dia_servicio = DiaServicio.objects.get(id=dia_servicio_id)
    
    # Obtener las visitas, anuncios y asistencias relacionadas con este Día de Servicio
    visitas = visita.objects.filter(dia_de_servicio=dia_servicio)
    anuncios = Anuncio.objects.filter(dia_de_servicio=dia_servicio)
    asistencias = Asistencia.objects.filter(dia_servicio=dia_servicio)
    
    # Renderizar el informe en la plantilla HTML
    return render(request, 'reportes/informe_dia_servicio.html', {
        'dia_servicio': dia_servicio,
        'visitas': visitas,
        'anuncios': anuncios,
        'asistencias': asistencias
    })


def detalles_dia_servicio(request, id):
    dia_servicio = get_object_or_404(DiaServicio, id=id)

    context = {
        'dia_servicio': dia_servicio,
    }

    return render(request, 'detalles_dia_servicio.html', context)