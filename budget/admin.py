from django.contrib import admin
from .models import Cuenta, Categoria, Presupuesto, Proyeccion, Gasto

# Personalización del modelo Cuenta en el panel de administración
class CuentaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'saldo_inicial', 'saldo_actual', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('nombre',)

    def saldo_actual(self, obj):
        return obj.saldo_actual
    saldo_actual.short_description = "Saldo Actual"

# Registro de modelos en el admin
admin.site.register(Categoria)
admin.site.register(Cuenta, CuentaAdmin)
admin.site.register(Presupuesto)
admin.site.register(Proyeccion)
admin.site.register(Gasto)
