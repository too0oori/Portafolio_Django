from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Proyecto, Habilidad, Perfil, Contacto
from .forms import ContactoForm


def index(request):
    """Vista principal del portafolio"""
    
    # Obtener perfil
    try:
        perfil = Perfil.objects.first()
    except Perfil.DoesNotExist:
        perfil = None
    
    # Obtener proyectos activos ordenados
    proyectos = Proyecto.objects.filter(activo=True).prefetch_related('imagenes')
    
    # Obtener habilidades por tipo
    habilidades_tecnicas = Habilidad.objects.filter(tipo='tecnica', activo=True)
    habilidades_personales = Habilidad.objects.filter(tipo='personal', activo=True)
    
    # Procesar formulario de contacto
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Mensaje enviado correctamente! Te responderé pronto.')
            return redirect('index')
        else:
            messages.error(request, 'Hubo un error al enviar el mensaje. Por favor, verifica los datos.')
    else:
        form = ContactoForm()
    
    context = {
        'perfil': perfil,
        'proyectos': proyectos,
        'habilidades_tecnicas': habilidades_tecnicas,
        'habilidades_personales': habilidades_personales,
        'form': form,
    }
    
    return render(request, 'index.html', context)