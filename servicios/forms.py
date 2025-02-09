from django import forms
from .models import DiaServicio, Servicio
from django.contrib import admin

class DiaServicioForm(forms.ModelForm):
    class Meta:
        model = DiaServicio
        fields = [
            'fecha_servicio',
            'tipo_de_servicio',
            'pastor',
            'tema',
            'versiculo_base',
            'numero_de_sillas',
            'numero_de_asistencia',
            'numero_de_carros',
            'numero_de_motos',
            'numero_de_bicicletas',
            'merienda',
            'numero_de_meriendas',
            'observaciones_reunion',
        ]



from .models import DiaServicio

"""
servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="dias_servicio")
    tipo_de_servicio = models.ForeignKey(TipoDeServicio, verbose_name=("Tipo de Servicio"), on_delete=models.CASCADE, null=True)
    numero_de_sillas = models.IntegerField(("Numero de Sillas"),null=True)
    numero_de_asistencia = models.IntegerField(("Numero de Asistencia"),null=True)
    pastor = models.ForeignKey(Miembro, on_delete=models.CASCADE,null=True)
    tema = models.CharField(("Tema"), max_length=50,null=True)
    versiculo_base = models.CharField(max_length=100,null=True)
    numero_de_carros = models.IntegerField(("Numero de Carros"),null=True)
    numero_de_motos = models.IntegerField(("Numero de Motos"),null=True)
    numero_de_bicicletas = models.IntegerField(("Numero de Bicicletas"),null=True)
    merienda = models.CharField(("Merienda"), max_length=50, null=True)
    numero_de_meriendas = models.IntegerField(("Numero de Meriendas Servidas"),null=True)

    fecha_servicio = models.DateField(auto_now=False, auto_now_add=False)
    observaciones_reunion = models.TextField(null=True)
"""


class DiaServicioForm(forms.ModelForm):
    class Meta:
        model = DiaServicio
        fields = 'tipo_de_servicio',  'pastor', 'tema','fecha_servicio', 'observaciones_reunion'
        widgets = {
            'observaciones_reunion': forms.Textarea(attrs={'cols': 30, 'rows': 5, 'style': 'width: 600px;'}),
        }


from django.contrib.admin.widgets import ForeignKeyRawIdWidget



class ServicioForm2(forms.ModelForm):
    dia_servicio = forms.ModelChoiceField(
        queryset=DiaServicio.objects.all(),
        widget=ForeignKeyRawIdWidget(DiaServicio._meta.get_field('id').remote_field, admin.site),
        label="Seleccionar Día de Servicio"
    )

    class Meta:
        model = Servicio
        fields = ('fecha_inicio', 'fecha_fin', 'equipo_de_servicio', 'dia_servicio')
        widgets = {
            'observaciones_reunion': forms.Textarea(attrs={'cols': 10, 'rows': 5, 'style': 'width: 50px;'}),
        }


class DiaServicioForm2(forms.ModelForm):
    class Meta:
        model = DiaServicio
        fields = ('servicio', 'tipo_de_servicio', 'fecha_servicio', 'observaciones_reunion')
        widgets = {
            'observaciones_reunion': forms.Textarea(attrs={'cols': 10, 'rows': 5, 'style': 'width: 250px;'}),
            'servicio': forms.Select(attrs={'style': 'width: 200px;'}),  # Selector para elegir el Servicio
        }

