from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .forms import DiaServicioForm, DiaServicioForm2, ServicioForm2

# Register your models here.
admin.site.site_header = "Iglesia de Cristo Monte Sión"
admin.site.site_title = "Sistema de Gestión Iglesia de Cristo Monte Sión"
admin.site.index_title = "Bienvenido al Administrador"



from .models import Anuncio, Aportacion, Asistencia, DiaServicio, Gasto, MovimientoInventario, Producto, Puesto, Miembro, Equipo, Servicio, TipoDeServicio,visita

class AsistenciaInline(admin.TabularInline):
    model = Asistencia
    extra = 0  # No agregar filas adicionales por defecto
    fields = ('miembro', 'aseo','servicio','excusa')  # Campos a mostrar en el formulario
    readonly_fields = ('miembro',)  # Hacer el campo 'miembro' solo lectura
    ordering = ['servicio']

class VisitaInline(admin.TabularInline):
    model = visita
    extra = 1


class DiaServicioInline(admin.TabularInline):
    model = DiaServicio
    extra = 1
    fields = ('tipo_de_servicio', 'fecha_servicio', 'observaciones_reunion', 'editar')  # Incluye el campo personalizado
    readonly_fields = ('editar',)  # Marca el campo 'editar' como solo lectura

    def editar(self, obj):
        if obj.pk:  # Verifica que el objeto ya esté guardado en la base de datos
            url = reverse('admin:servicios_diaservicio_change', args=[obj.pk])
            return format_html('<a href="{}" class="button">Editar</a>', url)
        return ''  # Si el objeto no tiene PK, está vacío (nuevo)

    editar.short_description = 'Editar'  # Título de la columna personalizada



      # Cambia el título del encabezado
     # Cambia el título del encabezado
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'inventario_actual')  # Mostrar el inventario actual calculado

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'fecha', 'tipo_movimiento')

@admin.action(description="Generar lista de asistencia")
def generar_lista_asistencia(modeladmin, request, queryset):
    for dia_servicio in queryset:
        servicio = dia_servicio.servicio
        equipo = servicio.equipo_de_servicio
        miembros = equipo.miembros.all()  # Obtener miembros del equipo

        # Crear asistencia para cada miembro
        for miembro in miembros:
            Asistencia.objects.get_or_create(dia_servicio=dia_servicio, miembro=miembro)
    modeladmin.message_user(request, "Lista de asistencia generada exitosamente.")

class AnuncioInline(admin.TabularInline):
    model = Anuncio
    extra = 1



# Registro en el admin
@admin.register(DiaServicio)
class DiaServicioAdmin(admin.ModelAdmin):

    list_display = ('__str__','fecha_servicio', 'servicio')
    
    inlines = [AsistenciaInline, VisitaInline, AnuncioInline]  # Agregar las asistencias como inline
    form = DiaServicioForm
    
    actions = [generar_lista_asistencia]
    

class AportacionInline(admin.TabularInline):
    model = Aportacion
    extra = 0  # No agregar filas adicionales por defecto
    fields = ('miembro', 'cantidad')  # Campos a mostrar en el formulario
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filtrar el campo 'miembro' según el equipo del servicio seleccionado.
        """
        if db_field.name == "miembro":
            # Obtener el servicio actualmente en edición
            servicio_id = request.resolver_match.kwargs.get('object_id')
            if servicio_id:
                servicio = Servicio.objects.get(id=servicio_id)
                # Filtrar los miembros que pertenecen al equipo del servicio
                kwargs['queryset'] = servicio.equipo_de_servicio.miembros.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
class GastoInline(admin.TabularInline):
    model = Gasto
    extra = 0
    fields = ('descripcion', 'cantidad', 'fecha_gasto')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filtrar el campo 'Servicio' según el equipo del servicio seleccionado.
        """
        if db_field.name == "Servicio":
            servicio_id = request.resolver_match.kwargs.get('object_id')
            if servicio_id:
                servicio = Servicio.objects.get(id=servicio_id)
                # Filtrar los servicios por equipo (este es un ejemplo, depende de tu estructura)
                kwargs['queryset'] = Servicio.objects.filter(equipo_de_servicio=servicio.equipo_de_servicio)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)    

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('fecha_inicio', 'fecha_fin', 'equipo_de_servicio')
    inlines = [DiaServicioInline, AportacionInline, GastoInline]
    raw_id_fields = ('equipo_de_servicio',)
    # Agregar las aportaciones como inline

# Registrar los modelos básicos
admin.site.register(TipoDeServicio)
admin.site.register(Puesto)
admin.site.register(Miembro)
admin.site.register(Equipo)
admin.site.register(Aportacion)
admin.site.register(visita)
admin.site.register(Asistencia)

