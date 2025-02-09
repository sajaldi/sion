from django.db import models
from django.db.models import Sum


# Categoría para clasificar proyecciones y gastos
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

# Cuenta para manejar saldos y transacciones
class Cuenta(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Cuenta")
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Saldo Inicial")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    @property
    def saldo_actual(self):
        # Obtiene la suma total de los costos de los gastos asociados a esta cuenta
        gastos_totales = self.gastos.aggregate(total=Sum('costo'))['total'] or 0
        # Calcula el saldo actual restando los gastos del saldo inicial
        return self.saldo_inicial - gastos_totales


    def __str__(self):
        return f"{self.nombre} - Saldo: {self.saldo_inicial}"

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"
        ordering = ["-fecha_creacion"]

# Presupuesto para gestionar periodos y categorías presupuestarias
class Presupuesto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Presupuesto")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Fin")

    def __str__(self):
        return f"{self.nombre} ({self.fecha_inicio} - {self.fecha_fin})"

    class Meta:
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"
        ordering = ["-fecha_inicio"]

# Proyección de gastos o ingresos en base a categorías
class Proyeccion(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name="Descripción")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="proyecciones", verbose_name="Categoría")
    cantidad_proyectada = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad Proyectada")

    def __str__(self):
        return f"{self.descripcion} - {self.categoria.nombre} - {self.cantidad_proyectada}"

    class Meta:
        verbose_name = "Proyección"
        verbose_name_plural = "Proyecciones"
        ordering = ["categoria", "descripcion"]

# Registro de gastos reales
class Gasto(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name="Descripción")
    proyeccion_inicial = models.ForeignKey(Proyeccion, on_delete=models.CASCADE, related_name="gastos", verbose_name="Proyección Relacionada")
    costo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo")
    fecha = models.DateField(verbose_name="Fecha del Gasto")
    cuenta = models.ForeignKey(Cuenta, on_delete=models.SET_NULL, null=True, blank=True, related_name="gastos", verbose_name="Cuenta Asociada")

    def __str__(self):
        return f"{self.descripcion} - {self.fecha} - {self.costo}"

    class Meta:
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"
        ordering = ["-fecha"]

