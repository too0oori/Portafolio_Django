from django.db import models
from django.core.validators import URLValidator

class Habilidad(models.Model):
    """Modelo para habilidades técnicas y personales"""
    TIPO_CHOICES = [
        ('tecnica', 'Técnica'),
        ('personal', 'Personal'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    icono = models.CharField(max_length=50, blank=True, help_text="Clase de Font Awesome o símbolo")
    orden = models.IntegerField(default=0, help_text="Orden de aparición")
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"
        ordering = ['tipo', 'orden']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class Proyecto(models.Model):
    """Modelo para proyectos del portafolio"""
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen_principal = models.ImageField(upload_to='proyectos/', help_text="Imagen principal del proyecto")
    
    # URLs
    url_codigo = models.URLField(validators=[URLValidator()], help_text="Link a GitHub")
    url_demo = models.URLField(blank=True, null=True, help_text="Link al sitio desplegado (opcional)")
    
    # Tecnologías
    tecnologias = models.CharField(max_length=300, help_text="Separadas por coma: Python, Django, Bootstrap")
    
    # Metadata
    orden = models.IntegerField(default=0, help_text="Orden de aparición (menor = primero)")
    destacado = models.BooleanField(default=False, help_text="Mostrar en la sección principal")
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['orden', '-fecha_creacion']
    
    def __str__(self):
        return self.titulo
    
    def get_tecnologias_list(self):
        """Retorna lista de tecnologías para el template"""
        return [tech.strip() for tech in self.tecnologias.split(',')]


class ImagenProyecto(models.Model):
    """Imágenes adicionales para el carrusel de cada proyecto"""
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='proyectos/capturas/')
    descripcion = models.CharField(max_length=200, help_text="Descripción de la captura")
    orden = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Imagen de Proyecto"
        verbose_name_plural = "Imágenes de Proyectos"
        ordering = ['orden']
    
    def __str__(self):
        return f"{self.proyecto.titulo} - {self.descripcion}"


class Contacto(models.Model):
    """Modelo para mensajes de contacto"""
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ['-fecha_envio']
    
    def __str__(self):
        return f"{self.nombre} - {self.fecha_envio.strftime('%d/%m/%Y')}"


class Perfil(models.Model):
    """Información del perfil principal (Solo debe haber 1 registro)"""
    nombre_completo = models.CharField(max_length=100, default="Sofía Lagos")
    apodo = models.CharField(max_length=50, default="tori")
    titulo = models.CharField(max_length=200, default="desarrolladora full stack python · artista visual")
    descripcion = models.TextField()
    
    # Redes sociales
    github_url = models.URLField(default="https://github.com/too0oori")
    linkedin_url = models.URLField(blank=True, null=True)
    email = models.EmailField(default="sofia.lagos.cesped@gmail.com")
    
    # Ilustración de contacto
    ilustracion_contacto = models.ImageField(upload_to='perfil/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfil"
    
    def __str__(self):
        return self.nombre_completo
    
    def save(self, *args, **kwargs):
        """Asegura que solo exista un perfil"""
        if not self.pk and Perfil.objects.exists():
            raise ValueError('Solo puede existir un perfil. Edita el existente.')
        return super().save(*args, **kwargs)