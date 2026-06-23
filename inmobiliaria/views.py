from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Perfil, Propiedad, Contrato


# -------------------------
# LOGIN
# -------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            perfil = Perfil.objects.filter(usuario=user).first()

            if not perfil:
                return render(request, "login.html", {
                    "error": "Usuario sin rol asignado"
                })

            return redirect("inicio")

        return render(request, "login.html", {
            "error": "Usuario o contraseña incorrectos"
        })

    return render(request, "login.html")


# -------------------------
# LOGOUT
# -------------------------
def logout_view(request):
    logout(request)
    return redirect("login")


# -------------------------
# INICIO ÚNICO (ADMIN + AGENTE)
# -------------------------
@login_required
def inicio(request):
    perfil = Perfil.objects.filter(usuario=request.user).first()

    if not perfil:
        return redirect("login")

    propiedades = Propiedad.objects.all()
    contratos = Contrato.objects.all()

    context = {
        "rol": perfil.rol,
        "propiedades": propiedades,
        "contratos": contratos,
    }

    # 🔥 SOLO ADMIN VE ESTADÍSTICAS
    if perfil.rol == "admin":
        context["total_propiedades"] = propiedades.count()
        context["total_contratos"] = contratos.count()

    return render(request, "inicio.html", context)

# -------------------------
# PROPIEDADES
# -------------------------

@login_required
def listarPropiedades(request):
    propiedades = Propiedad.objects.all()

    return render(
        request,
        'listarPropiedades.html',
        {'propiedades': propiedades}
    )


@login_required
def nuevaPropiedad(request):
    return render(request, 'nuevaPropiedad.html')


@login_required
def guardarPropiedad(request):

    foto = request.FILES.get('foto')

    Propiedad.objects.create(
        agente=request.user,
        foto=foto,
        direccion=request.POST['direccion'],
        tipo=request.POST['tipo'],
        operacion=request.POST['operacion'],
        precio=request.POST['precio'],
        estacionamiento='estacionamiento' in request.POST
    )

    return redirect('listarPropiedades')


@login_required
def editarPropiedad(request, id):
    propiedad = Propiedad.objects.get(id=id)

    return render(
        request,
        'editarPropiedad.html',
        {'propiedad': propiedad}
    )


@login_required
def actualizarPropiedad(request):

    propiedad = Propiedad.objects.get(
        id=request.POST['id']
    )

    propiedad.direccion = request.POST['direccion']
    propiedad.tipo = request.POST['tipo']
    propiedad.operacion = request.POST['operacion']
    propiedad.precio = request.POST['precio']
    propiedad.estacionamiento = 'estacionamiento' in request.POST

    nuevaFoto = request.FILES.get('foto')

    if nuevaFoto:
        propiedad.foto = nuevaFoto

    propiedad.save()

    return redirect('listarPropiedades')


@login_required
def eliminarPropiedad(request, id):
    propiedad = Propiedad.objects.get(id=id)
    propiedad.delete()

    return redirect('listarPropiedades')

# -------------------------
# CONTRATOS
# -------------------------

@login_required
def listarContratos(request):
    contratos = Contrato.objects.all()
    return render(
        request, 
        'listarContratos.html', 
        {'contratos': contratos}
    )

@login_required
def nuevoContrato(request):
    propiedades = Propiedad.objects.all()
    return render(
        request, 
        'nuevoContrato.html', 
        {'propiedades': propiedades}
    )

@login_required
def guardarContrato(request):
    propiedad = Propiedad.objects.get(id=request.POST['propiedad_id'])
    
    Contrato.objects.create(
        propiedad=propiedad,
        inquilino=request.POST['inquilino'],
        archivo_pdf=request.FILES.get('archivo_pdf'),
        fecha_firma=request.POST['fecha_firma'],
        fecha_vencimiento=request.POST['fecha_vencimiento'],
        plazo_meses=request.POST['plazo_meses'],
        aval_requerido='aval_requerido' in request.POST,
        creado_por=request.user
    )
    
    return redirect('listarContratos')

@login_required
def editarContrato(request, id):
    contrato = Contrato.objects.get(id=id)
    propiedades = Propiedad.objects.all()
    return render(
        request, 
        'editarContrato.html', 
        {'contrato': contrato, 'propiedades': propiedades}
    )

@login_required
def actualizarContrato(request):
    contrato = Contrato.objects.get(id=request.POST['id'])
    
    contrato.propiedad = Propiedad.objects.get(id=request.POST['propiedad_id'])
    contrato.inquilino = request.POST['inquilino']
    contrato.fecha_firma = request.POST['fecha_firma']
    contrato.fecha_vencimiento = request.POST['fecha_vencimiento']
    contrato.plazo_meses = request.POST['plazo_meses']
    contrato.aval_requerido = 'aval_requerido' in request.POST
    
    archivo = request.FILES.get('archivo_pdf')
    if archivo:
        contrato.archivo_pdf = archivo
        
    contrato.save()
    return redirect('listarContratos')

@login_required
def eliminarContrato(request, id):
    contrato = Contrato.objects.get(id=id)
    contrato.delete()
    return redirect('listarContratos')