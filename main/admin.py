from django.contrib import admin
from .models import Habilidad, Proyecto, ImagenProyecto, Contacto, Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'apodo', 'email')
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre_completo', 'apodo', 'titulo', 'descripcion')
        }),
        ('Redes Sociales', {
            'fields': ('github_url', 'linkedin_url', 'email')
        }),
        ('Recursos', {
            'fields': ('ilustracion_contacto',)
        }),
    )
    
    def has_add_permission(self, request):
        """Evita crear más de un perfil"""
        if Perfil.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        """Evita eliminar el perfil"""
        return False


class ImagenProyectoInline(admin.TabularInline):
    model = ImagenProyecto
    extra = 1
    fields = ('imagen', 'descripcion', 'orden')


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'destacado', 'activo', 'orden', 'fecha_creacion')
    list_filter = ('destacado', 'activo', 'fecha_creacion')
    list_editable = ('destacado', 'activo', 'orden')
    search_fields = ('titulo', 'descripcion', 'tecnologias')
    inlines = [ImagenProyectoInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'imagen_principal')
        }),
        ('Enlaces', {
            'fields': ('url_codigo', 'url_demo')
        }),
        ('Tecnologías', {
            'fields': ('tecnologias',),
            'description': 'Ingresa las tecnologías separadas por comas. Ej: Python, Django, Bootstrap'
        }),
        ('Configuración', {
            'fields': ('orden', 'destacado', 'activo')
        }),
    )


@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'icono', 'orden', 'activo')
    list_filter = ('tipo', 'activo')
    list_editable = ('orden', 'activo')
    search_fields = ('nombre',)
    
    fieldsets = (
        (None, {
            'fields': ('nombre', 'tipo', 'icono', 'orden', 'activo')
        }),
    )


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'fecha_envio', 'leido')
    list_filter = ('leido', 'fecha_envio')
    list_editable = ('leido',)
    search_fields = ('nombre', 'email', 'mensaje')
    readonly_fields = ('nombre', 'email', 'mensaje', 'fecha_envio')
    
    fieldsets = (
        ('Información del Remitente', {
            'fields': ('nombre', 'email', 'fecha_envio')
        }),
        ('Mensaje', {
            'fields': ('mensaje',)
        }),
        ('Estado', {
            'fields': ('leido',)
        }),
    )
    
    def has_add_permission(self, request):
        """Los mensajes solo se crean desde el formulario público"""
        return False