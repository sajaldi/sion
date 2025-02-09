# urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
urlpatterns = [
    path('informe_asistencia/<int:dia_servicio_id>/', views.informe_asistencia, name='informe_asistencia'),
    path('reporte_asistencia_pdf/<int:dia_servicio_id>/', views.reporte_asistencia_pdf, name='reporte_asistencia_pdf'),
    path('reporte_asistencia_html/<int:dia_servicio_id>/', views.reporte_asistencia_html, name='reporte_asistencia_html'),
    path('informe/<int:dia_servicio_id>/', views.generar_informe_dia_servicio, name='informe_dia_servicio'),
    path('editar-dia-servicio/<int:id>/', views.editar_dia_servicio, name='editar_dia_servicio'),
    path('detalles-dia-servicio/<int:id>/', views.detalles_dia_servicio, name='detalles_dia_servicio'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
