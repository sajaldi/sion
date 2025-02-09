from django.db import models

####Puesto
class Puesto(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
####Clase Miembros 

class Miembro ( models.Model):
    nombre = models.CharField(max_length=100)
    puesto = models.ForeignKey(Puesto,on_delete=models.CASCADE)
    telefono = models.CharField(max_length=50, null=True)
    direccion = models.CharField(max_length=150, null=True)
    primera_visita = models.DateField(null=True, auto_now=False, auto_now_add=False)
    fecha_de_nacimiento = models.DateField(null=True, auto_now=False, auto_now_add=False)
    foto = models.ImageField( height_field=None, width_field=None, max_length=None)
    def __str__(self):
        return self.nombre
####Clase Equipo

class Equipo (models.Model):
    nombre = models.CharField(max_length=100)
    miembros = models.ManyToManyField(Miembro,related_name='equipos')

    def __str__(self):
        return self.nombre

class Checklist (models.Model):
    nombre = models.CharField(max_length=100)

class DetalleChecklist (models.Model):
    detalle = models.CharField(max_length=100)
    Checklist = models.ForeignKey(Checklist,on_delete=models.CASCADE)



class Servicio(models.Model):
    fecha_inicio = models.DateField(auto_now=False, auto_now_add=False)
    fecha_fin = models.DateField(auto_now=False, auto_now_add=False)
    equipo_de_servicio = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    def __str__(self):
        return f"Servicio del {self.fecha_inicio} al {self.fecha_fin} - {self.equipo_de_servicio}"
class TipoDeServicio (models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre
    
class DiaServicio(models.Model):
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
    def __str__(self):
        return f"{self.fecha_servicio} ({self.tipo_de_servicio})"

class visita ( models.Model):
    nombre = models.CharField(max_length=50)
    dia_de_servicio =models.ForeignKey(DiaServicio, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.nombre

    

class Asistencia(models.Model):
    dia_servicio = models.ForeignKey(DiaServicio, on_delete=models.CASCADE, related_name="asistencias")
    miembro = models.ForeignKey('Miembro', on_delete=models.CASCADE)
    aseo = models.BooleanField(default=False)
    servicio = models.BooleanField(default=False)
    excusa = models.BooleanField(default=False)
    def __str__(self):
        return f"Asistencia de {self.miembro.nombre} el {self.dia_servicio.fecha_servicio}"
    
class Aportacion(models.Model):
    miembro = models.ForeignKey(Miembro, verbose_name=("Nombre"), on_delete=models.CASCADE)
    Servicio = models.ForeignKey(Servicio,on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
       return f"{self.miembro}"
class Gasto(models.Model):
    descripcion = models.CharField(("descripcion del gasto"), max_length=50) # type: ignore
    cantidad = models.DecimalField(("Costo"), max_digits=5, decimal_places=2) # type: ignore
    fecha_gasto = models.DateField(("Fecha del Gasto"), auto_now=False, auto_now_add=False)
    Servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    def __str__(self):
        return self.nombre
    
    @property
    def inventario_actual(self):
        # Obtener los movimientos de inventario del producto
        ingresos = MovimientoInventario.objects.filter(producto=self, tipo_movimiento=MovimientoInventario.INGRESO)
        salidas = MovimientoInventario.objects.filter(producto=self, tipo_movimiento=MovimientoInventario.SALIDA)
        ajustes = MovimientoInventario.objects.filter(producto=self, tipo_movimiento=MovimientoInventario.AJUSTE)

        # Sumar los ingresos y restar las salidas, considerando los ajustes
        inventario = (
            sum([movimiento.cantidad for movimiento in ingresos]) - 
            sum([movimiento.cantidad for movimiento in salidas]) +
            sum([movimiento.cantidad for movimiento in ajustes])
        )
        
        return inventario
class MovimientoInventario(models.Model):
    INGRESO = 'ING'
    SALIDA = 'SAL'
    AJUSTE = 'AJU'
     
    TIPO_MOVIMIENTO_CHOICES = [
        (INGRESO, 'Ingreso'),
        (SALIDA, 'Salida'),
        (AJUSTE, 'Ajuste'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField( auto_now=False, auto_now_add=False)
    tipo_movimiento = models.CharField(
        max_length=3,
        choices=TIPO_MOVIMIENTO_CHOICES,
        default=INGRESO,  # Valor predeterminado: Ingreso
    )
    def __str__(self):
        return f"{self.producto} -  {self.cantidad} - {self.get_tipo_movimiento_display() }"
    

class Anuncio(models.Model):
    anuncio = models.CharField(max_length=300)
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    dia_de_servicio = models.ForeignKey(DiaServicio, on_delete=models.CASCADE)
