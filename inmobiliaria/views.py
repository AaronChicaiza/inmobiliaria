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