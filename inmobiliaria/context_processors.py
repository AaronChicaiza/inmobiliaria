from .models import Perfil

def rol_usuario(request):
    if not request.user.is_authenticated:
        return {"rol": None}

    try:
        perfil = Perfil.objects.get(usuario=request.user)
        return {"rol": perfil.rol}
    except Perfil.DoesNotExist:
        return {"rol": None}