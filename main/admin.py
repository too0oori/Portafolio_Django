from django.contrib import admin
from django.utils.html import format_html
from .models import Habilidad, Proyecto, ImagenProyecto, Contacto, Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    """Administración del perfil personal"""
    list_display = ('nombre_completo', 'apodo', 'email', 'ver_sitio')
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre_completo', 'apodo', 'titulo', 'descripcion'),
            'description': 'Información básica que aparece en la página principal'
        }),
        ('Redes Sociales', {
            'fields': ('github_url', 'linkedin_url', 'email'),
            'description': 'Enlaces a redes sociales y contacto'
        }),
        ('Recursos Visuales', {
            'fields': ('ilustracion_contacto',),
            'description': 'Imagen que aparece en la sección de contacto'
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
    
    def ver_sitio(self, obj):
        """Botón para ver el sitio"""
        return format_html(
            '<a href="/" target="_blank" class="button">Ver sitio 🔗</a>'
        )
    ver_sitio.short_description = 'Acciones'


class ImagenProyectoInline(admin.TabularInline):
    """Inline para agregar múltiples imágenes a un proyecto"""
    model = ImagenProyecto
    extra = 1
    fields = ('imagen', 'descripcion', 'orden')
    
    def has_delete_permission(self, request, obj=None):
        """Evita eliminar imágenes"""
        return False


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    """Administración de proyectos del portafolio"""
    list_display = (
        'titulo', 
        'es_destacado', 
        'estado', 
        'orden', 
        'cantidad_imagenes',
        'fecha_creacion',
        'acciones'
    )
    list_filter = ('destacado', 'activo', 'fecha_creacion')
    list_editable = ('orden',)
    search_fields = ('titulo', 'descripcion', 'tecnologias')
    inlines = [ImagenProyectoInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'imagen_principal'),
            'description': 'Título, descripción e imagen principal del proyecto'
        }),
        ('Enlaces', {
            'fields': ('url_codigo', 'url_demo'),
            'description': 'Enlaces al repositorio y demo en vivo'
        }),
        ('Tecnologías', {
            'fields': ('tecnologias',),
            'description': '💡 Ingresa las tecnologías separadas por comas. Ej: Python, Django, Bootstrap'
        }),
        ('Configuración de Visualización', {
            'fields': ('orden', 'destacado', 'activo'),
            'description': '⭐ Proyectos destacados aparecen en la página principal'
        }),
    )
    
    def es_destacado(self, obj):
        """Muestra si el proyecto es destacado con emoji"""
        if obj.destacado:
            return format_html('<span style="color: #dc2626;">⭐ Destacado</span>')
        return '○ Normal'
    es_destacado.short_description = 'Tipo'
    
    def estado(self, obj):
        """Muestra el estado del proyecto con color"""
        if obj.activo:
            return format_html('<span style="color: #16a34a;">✓ Activo</span>')
        return format_html('<span style="color: #dc2626;">✗ Inactivo</span>')
    estado.short_description = 'Estado'
    
    def cantidad_imagenes(self, obj):
        """Cuenta cuántas imágenes tiene el proyecto"""
        count = obj.imagenes.count()
        if count > 0:
            return format_html(f'<span style="color: #2563eb;">📸 {count}</span>')
        return '0'
    cantidad_imagenes.short_description = 'Imágenes'
    
    def acciones(self, obj):
        """Botones de acción rápida"""
        return format_html(
            '<a href="{}" target="_blank" class="button">Ver en sitio 🔗</a>',
            '/#proyectos' if obj.destacado else '/proyectos/'
        )
    acciones.short_description = 'Acciones'
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }


@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    """Administración de habilidades técnicas y personales"""
    list_display = ('nombre', 'tipo_badge', 'icono', 'orden', 'estado', 'vista_previa')
    list_filter = ('tipo', 'activo')
    list_editable = ('orden',)
    search_fields = ('nombre',)
    
    fieldsets = (
        ('Información de la Habilidad', {
            'fields': ('nombre', 'tipo', 'icono'),
            'description': '💡 Para el icono usa clases de Font Awesome (ej: fas fa-python) o emojis (ej: 🐍)'
        }),
        ('Configuración', {
            'fields': ('orden', 'activo'),
            'description': 'El orden determina en qué posición aparece'
        }),
    )
    
    def tipo_badge(self, obj):
        """Muestra el tipo de habilidad con badge colorido"""
        if obj.tipo == 'tecnica':
            return format_html('<span style="background: #dc2626; color: white; padding: 4px 8px; border-radius: 4px;">💻 Técnica</span>')
        return format_html('<span style="background: #2563eb; color: white; padding: 4px 8px; border-radius: 4px;">🧠 Personal</span>')
    tipo_badge.short_description = 'Tipo'
    
    def estado(self, obj):
        """Muestra el estado con color"""
        if obj.activo:
            return format_html('<span style="color: #16a34a;">✓ Activa</span>')
        return format_html('<span style="color: #dc2626;">✗ Inactiva</span>')
    estado.short_description = 'Estado'
    
    def vista_previa(self, obj):
        """Muestra cómo se verá la habilidad"""
        return format_html(
            '<div style="padding: 8px 12px; background: #f3f4f6; border-radius: 4px; display: inline-block;">'
            '{} {}</div>',
            obj.icono,
            obj.nombre
        )
    vista_previa.short_description = 'Vista Previa'


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    """Administración de mensajes de contacto"""
    list_display = ('nombre', 'email', 'fecha_envio', 'estado_leido', 'acciones')
    list_filter = ('leido', 'fecha_envio')
    search_fields = ('nombre', 'email', 'mensaje')
    readonly_fields = ('nombre', 'email', 'mensaje', 'fecha_envio', 'mensaje_formateado')
    date_hierarchy = 'fecha_envio'
    
    fieldsets = (
        ('Información del Remitente', {
            'fields': ('nombre', 'email', 'fecha_envio')
        }),
        ('Mensaje', {
            'fields': ('mensaje_formateado',),
            'description': 'Contenido del mensaje recibido'
        }),
        ('Estado', {
            'fields': ('leido',),
            'description': 'Marca como leído cuando hayas respondido'
        }),
    )
    
    def has_add_permission(self, request):
        """Los mensajes solo se crean desde el formulario público"""
        return False
    
    def estado_leido(self, obj):
        """Muestra si el mensaje ha sido leído"""
        if obj.leido:
            return format_html('<span style="color: #16a34a;">✓ Leído</span>')
        return format_html('<span style="color: #dc2626; font-weight: bold;">✉ Nuevo</span>')
    estado_leido.short_description = 'Estado'
    
    def acciones(self, obj):
        """Botón para responder por email"""
        return format_html(
            '<a href="mailto:{}?subject=Re: Mensaje desde portafolio" class="button">Responder 📧</a>',
            obj.email
        )
    acciones.short_description = 'Acciones'
    
    def mensaje_formateado(self, obj):
        """Muestra el mensaje con mejor formato"""
        return format_html(
            '<div style="background: #f3f4f6; padding: 16px; border-radius: 8px; '
            'border-left: 4px solid #dc2626; white-space: pre-wrap;">{}</div>',
            obj.mensaje
        )
    mensaje_formateado.short_description = 'Mensaje'
    
    # Configurar las acciones personalizadas
    actions = ['marcar_como_leido', 'marcar_como_no_leido']
    
    def marcar_como_leido(self, request, queryset):
        """Acción masiva para marcar mensajes como leídos"""
        updated = queryset.update(leido=True)
        self.message_user(request, f'{updated} mensaje(s) marcado(s) como leído(s).')
    marcar_como_leido.short_description = '✓ Marcar como leído'
    
    def marcar_como_no_leido(self, request, queryset):
        """Acción masiva para marcar mensajes como no leídos"""
        updated = queryset.update(leido=False)
        self.message_user(request, f'{updated} mensaje(s) marcado(s) como no leído(s).')
    marcar_como_no_leido.short_description = '✉ Marcar como no leído'


# Personalización del sitio de administración
admin.site.site_header = "Administración · Portafolio Sofía [tori]"
admin.site.site_title = "Admin Portafolio"
admin.site.index_title = "Panel de Control del Portafolio"