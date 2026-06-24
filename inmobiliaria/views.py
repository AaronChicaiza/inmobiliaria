from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Perfil, Propiedad, Contrato, PagoRenta
from datetime import date, timedelta
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Sum


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

    messages.success(request, "Propiedad creada correctamente")
    return redirect('listarPropiedades')

@login_required
def editarPropiedad(request, id):
    propiedad = get_object_or_404(Propiedad, id=id)

    return render(
        request,
        'editarPropiedad.html',
        {'propiedad': propiedad}
    )


@login_required
def actualizarPropiedad(request):

    propiedad = get_object_or_404(Propiedad, id=request.POST['id'])

    propiedad.direccion = request.POST['direccion']
    propiedad.tipo = request.POST['tipo']
    propiedad.operacion = request.POST['operacion']
    propiedad.precio = float(request.POST['precio'])
    propiedad.estacionamiento = 'estacionamiento' in request.POST

    nuevaFoto = request.FILES.get('foto')

    if nuevaFoto and nuevaFoto.size > 0:
        propiedad.foto = nuevaFoto

    propiedad.save()

    messages.success(request, "Propiedad actualizada correctamente")
    return redirect('listarPropiedades')


@login_required
def eliminarPropiedad(request, id):
    propiedad = get_object_or_404(Propiedad, id=id)
    propiedad.delete()

    messages.success(request, "Propiedad eliminada correctamente")
    return redirect('listarPropiedades')
# -------------------------
# CONTRATOS
# -------------------------

@login_required
def listarContratos(request):
    contratos = Contrato.objects.all()
    return render(request, 'listarContratos.html', {'contratos': contratos})

@login_required
def nuevoContrato(request):
    propiedades = Propiedad.objects.all()
    return render(request, 'nuevoContrato.html', {'propiedades': propiedades})

@login_required
def guardarContrato(request):
    if request.method == 'POST':
        archivo = request.FILES.get('archivo_pdf')
        
        # Validación de seguridad: solo PDF
        if archivo and not archivo.name.lower().endswith('.pdf'):
            messages.error(request, "Error: Solo se permiten archivos en formato PDF.")
            return redirect('nuevoContrato')

        propiedad = get_object_or_404(Propiedad, id=request.POST.get('propiedad_id'))
        
        Contrato.objects.create(
            propiedad=propiedad,
            inquilino=request.POST.get('inquilino'),
            archivo_pdf=archivo,
            fecha_firma=request.POST.get('fecha_firma'),
            fecha_vencimiento=request.POST.get('fecha_vencimiento'),
            plazo_meses=request.POST.get('plazo_meses'),
            aval_requerido='aval_requerido' in request.POST,
            creado_por=request.user
        )
        
        messages.success(request, "Contrato registrado con éxito.")
        return redirect('listarContratos')

@login_required
def editarContrato(request, id):
    contrato = get_object_or_404(Contrato, id=id)
    propiedades = Propiedad.objects.all()
    return render(request, 'editarContrato.html', {'contrato': contrato, 'propiedades': propiedades})

@login_required
def actualizarContrato(request):
    if request.method == 'POST':
        contrato = get_object_or_404(Contrato, id=request.POST.get('id'))
        archivo = request.FILES.get('archivo_pdf')

        # Validación de formato PDF
        if archivo and not archivo.name.lower().endswith('.pdf'):
            messages.error(request, "Error: Solo se permiten archivos PDF.")
            return redirect('editarContrato', id=contrato.id)
        
        # Actualización de datos básicos
        contrato.propiedad = get_object_or_404(Propiedad, id=request.POST.get('propiedad_id'))
        contrato.inquilino = request.POST.get('inquilino')
        contrato.fecha_firma = request.POST.get('fecha_firma')
        contrato.fecha_vencimiento = request.POST.get('fecha_vencimiento')
        contrato.plazo_meses = request.POST.get('plazo_meses')
        contrato.aval_requerido = 'aval_requerido' in request.POST
        
        # Lógica de reemplazo de archivo PDF
        if archivo:
            # Si ya existía un archivo, lo eliminamos físicamente primero
            if contrato.archivo_pdf:
                contrato.archivo_pdf.delete(save=False)
            
            # Asignamos el nuevo archivo
            contrato.archivo_pdf = archivo
            
        contrato.save()
        messages.success(request, "Contrato actualizado correctamente.")
        return redirect('listarContratos')

@login_required
def eliminarContrato(request, id):
    contrato = get_object_or_404(Contrato, id=id)
    
    # Eliminación física del archivo PDF antes de borrar el registro
    if contrato.archivo_pdf:
        contrato.archivo_pdf.delete(save=False)
        
    contrato.delete()
    messages.success(request, "Contrato eliminado correctamente.")
    return redirect('listarContratos')

@login_required
def contratosPorVencer(request):
    hoy = date.today()
    fecha_limite = hoy + timedelta(days=30)
    contratos = Contrato.objects.filter(fecha_vencimiento__range=[hoy, fecha_limite])
    return render(request, 'contratosPorVencer.html', {'contratos': contratos})

def reporte_ingresos(request):
    pagos = PagoRenta.objects.select_related(
        'contrato',
        'contrato__propiedad'
    ).all()

    total_ingresos = pagos.aggregate(
        total=Sum('monto')
    )['total'] or 0

    return render(request, 'reporteIngresos.html', {
        'pagos': pagos,
        'total_ingresos': total_ingresos
    })


def reporte_ocupacion(request):
    total_propiedades = Propiedad.objects.count()
    rentadas = Contrato.objects.values('propiedad').distinct().count()

    vacias = total_propiedades - rentadas

    porcentaje = (rentadas / total_propiedades * 100) if total_propiedades else 0

    return render(request, 'reporteOcupacion.html', {
        'porcentaje_ocupacion': round(porcentaje, 1),
        'propiedades_rentadas': rentadas,
        'propiedades_vacias': vacias
    })



def crear_pago(request):
    contratos = Contrato.objects.all()

    print("CONTRATOS:", contratos)  # 🔥 DEBUG

    if request.method == "POST":
        contrato_id = request.POST.get('contrato')
        monto = request.POST.get('monto')
        mes = request.POST.get('mes_correspondiente')

        contrato = get_object_or_404(Contrato, id=contrato_id)

        PagoRenta.objects.create(
            contrato=contrato,
            monto=monto,
            mes_correspondiente=mes
        )

        messages.success(request, "Pago registrado correctamente")
        return redirect('reporte_ingresos')

    return render(request, 'crearPago.html', {
        'contratos': contratos
    })

def eliminar_pago(request, id):
    pago = get_object_or_404(PagoRenta, id=id)
    pago.delete()
    return redirect('reporte_ingresos')