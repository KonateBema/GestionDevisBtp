# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Devis, LigneDevis, Projet, Materiau
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.models import User, Group
from django.shortcuts import  get_object_or_404
from .models import Projet, Client
from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('home')

            elif user.groups.filter(name='Agent').exists():
                return redirect('home')

            elif user.groups.filter(name='Client').exists():
                return redirect('home')

            return redirect('home')

        return render(request, 'login.html', {'error': 'Identifiants invalides'})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def assign_role(user, role_name):
    group = Group.objects.get(name=role_name)
    user.groups.add(group)


def is_agent(user):
    return user.groups.filter(name='Agent').exists()


@user_passes_test(is_agent)
def dashboard_agent(request):
    return render(request, 'agent_dashboard.html')

@login_required
def home(request):
    if request.user.is_superuser:
        role = "Admin"
    elif request.user.groups.filter(name='Agent').exists():
        role = "Agent"
    else:
        role = "Client"

    return render(request, 'home.html', {'role': role})

from .models import Devis, Projet

from .models import Devis, LigneDevis, Projet, Materiau


def create_devis(request):

    projets = Projet.objects.all()
    materiaux = Materiau.objects.all()

    if request.method == "POST":

        projet = get_object_or_404(Projet, id=request.POST.get('projet'))

        # numéro auto simple
        numero = f"DEV-{Devis.objects.count() + 1:05d}"

        devis = Devis.objects.create(
            numero=numero,
            projet=projet,
            created_by=request.user
        )

        # =========================
        # 📦 LIGNES DYNAMIQUES
        # =========================
        i = 0
        while True:
            m_key = f"materiau_{i}"
            q_key = f"quantite_{i}"
            p_key = f"prix_{i}"

            if m_key not in request.POST:
                break

            materiau_id = request.POST.get(m_key)
            quantite = request.POST.get(q_key)
            prix = request.POST.get(p_key)

            if materiau_id and quantite and prix:

                LigneDevis.objects.create(
                    devis=devis,
                    materiau_id=materiau_id,
                    quantite=quantite,
                    prix_unitaire=prix
                )

            i += 1

        return redirect('devis_detail', id=devis.id)

    return render(request, 'create.html', {
        'projets': projets,
        'materiaux': materiaux
    })


def devis_list(request):
    devis = Devis.objects.all()
    return render(request, 'devis/list.html', {'devis': devis})





def devis_pdf(request, id):
    devis = Devis.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="devis_{devis.numero}.pdf"'

    p = canvas.Canvas(response)

    # ================= HEADER =================
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "GESTION DEVIS BTP")

    p.setFont("Helvetica", 12)
    p.drawString(50, 770, f"Numéro Devis : {devis.numero}")
    p.drawString(50, 750, f"Projet : {devis.projet.nom}")

    # ================= LIGNES =================
    y = 700

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Matériau")
    p.drawString(200, y, "Qté")
    p.drawString(300, y, "Prix")
    p.drawString(400, y, "Total")

    y -= 20

    total_general = 0

    for ligne in devis.lignes.all():

        total = ligne.quantite * ligne.prix_unitaire
        total_general += total

        p.setFont("Helvetica", 10)
        p.drawString(50, y, ligne.materiau.designation)
        p.drawString(200, y, str(ligne.quantite))
        p.drawString(300, y, str(ligne.prix_unitaire))
        p.drawString(400, y, str(total))

        y -= 20

    # ================= TOTAL =================
    p.setFont("Helvetica-Bold", 12)
    p.drawString(300, y - 20, "TOTAL GENERAL :")
    p.drawString(420, y - 20, str(total_general))

    p.showPage()
    p.save()

    return response


from .models import Devis

def dashboard(request):

    clients_count = Client.objects.count()
    projets = Projet.objects.all()
    devis_qs = Devis.objects.all()

    projets_count = projets.count()
    devis_count = devis_qs.count()

    total_ca = sum([d.total() if callable(d.total) else d.total for d in devis_qs])

    derniers_devis = devis_qs.order_by('-id')[:5]

    devis_brouillon = devis_qs.filter(statut="brouillon").count()
    devis_envoye = devis_qs.filter(statut="envoye").count()
    devis_accepte = devis_qs.filter(statut="accepte").count()
    devis_refuse = devis_qs.filter(statut="refuse").count()

    projets_retard = projets.filter(progression__lt=100)

    return render(request, 'dashboard.html', {
        'clients_count': clients_count,
        'projets_count': projets_count,
        'devis_count': devis_count,
        'total_ca': total_ca,

        'devis_brouillon': devis_brouillon,
        'devis_envoye': devis_envoye,
        'devis_accepte': devis_accepte,
        'devis_refuse': devis_refuse,

        'derniers_devis': derniers_devis,
        'projets': projets,
        'projets_retard': projets_retard,
    })

from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()


@user_passes_test(is_admin)
def admin_panel(request):
    return render(request, 'admin_panel.html')


import os
from django.http import HttpResponse
from datetime import datetime

def backup_db(request):
    file_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sqlite3"
    file_path = os.path.join(os.getcwd(), file_name)

    os.system(f"copy db.sqlite3 {file_path}")

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response

def users_list(request):
    users = User.objects.all()
    return render(request, 'users/list.html', {'users': users})

def create_user(request):

    groups = Group.objects.all()

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(
            username=username,
            password=password
        )

        group = Group.objects.get(name=role)
        user.groups.add(group)

        return redirect('users_list')

    return render(request, 'users/create.html', {'groups': groups})


from .models import Devis

def devis_detail(request, id):
    devis = get_object_or_404(Devis, id=id)

    return render(
        request,
        'detail.html',
        {'devis': devis}
    )

from django.contrib.auth.models import User

def toggle_user(request, id):
    user = get_object_or_404(User, id=id)

    user.is_active = not user.is_active
    user.save()

    return redirect('users_list')

def delete_user(request, id):
    user = get_object_or_404(User, id=id)

    # empêcher la suppression de son propre compte
    if request.user.id != user.id:
        user.delete()

    return redirect('users_list')


def projet_list(request):
    projets = Projet.objects.all()
    return render(request, "projet/list.html", {"projets": projets})

def create_projet(request):
    clients = Client.objects.all()

    if request.method == "POST":
        Projet.objects.create(
            client_id=request.POST["client"],
            nom=request.POST["nom"],
            localisation=request.POST["localisation"],
            date_debut=request.POST.get("date_debut") or None,
            budget=request.POST.get("budget") or 0,
            progression=request.POST.get("progression") or 0
        )
        # return redirect("projet_list")
        return redirect("liste_projets")
    return render(request, "projet/create.html", {
        "clients": clients
    })

from .models import Client
from django.shortcuts import render, redirect

def create_client(request):
    if request.method == "POST":
        nom = request.POST['nom']
        telephone = request.POST['telephone']
        email = request.POST.get('email', '')
        adresse = request.POST.get('adresse', '')

        Client.objects.create(
            nom=nom,
            telephone=telephone,
            email=email,
            adresse=adresse
        )

        # return redirect('dashboard')
        return redirect('liste_clients')

    return render(request, 'clients/create.html')

from .models import Materiau
from django.shortcuts import render, redirect, get_object_or_404

# 📦 LISTE MATERIAUX
def materiaux_list(request):
    materiaux = Materiau.objects.all()
    return render(request, 'materiaux/list.html', {'materiaux': materiaux})


# ➕ CREATION MATERIAU
def create_materiau(request):
    if request.method == "POST":
        Materiau.objects.create(
            designation=request.POST['designation'],
            unite=request.POST['unite'],
            prix_unitaire=request.POST['prix_unitaire']
        )
        return redirect('materiaux_list')

    return render(request, 'materiaux/create.html')

def liste_projets(request):
    projets = Projet.objects.select_related('client').all()

    return render(
        request,
        'projet/list.html',
        {'projets': projets}  # ✅ correct
    )

def edit_projet(request, id):
    projet = Projet.objects.get(id=id)
    clients = Client.objects.all()

    if request.method == "POST":
        projet.nom = request.POST["nom"]
        projet.localisation = request.POST["localisation"]
        projet.client_id = request.POST["client"]
        projet.date_debut = request.POST.get("date_debut") or None

        # ✅ CORRECTION ICI
        projet.budget = request.POST.get("budget") or 0
        projet.progression = request.POST.get("progression") or 0

        projet.save()

        return redirect("liste_projets")

    return render(request, "projet/edit.html", {
        "projet": projet,
        "clients": clients
    })


def delete_projet(request, id):
    projet = Projet.objects.get(id=id)
    projet.delete()
    return redirect("liste_projets")


def detail_projet(request, id):
    projet = Projet.objects.get(id=id)
    return render(request, "projet/detail.html", {
        "projet": projet,
        "documents": projet.documents.all()
    })

def upload_document(request, id):
    projet = Projet.objects.get(id=id)

    if request.method == "POST":
        DocumentProjet.objects.create(
            projet=projet,
            titre=request.POST.get("titre"),
            fichier=request.FILES["fichier"]
        )

    return redirect("detail_projet", id=id)

def clients(request):

    if request.method == "POST":
        Client.objects.create(
            nom=request.POST["nom"],
            telephone=request.POST["telephone"],
            email=request.POST.get("email"),
            adresse=request.POST.get("adresse")
        )
        return redirect("clients")

    clients = Client.objects.all().order_by("-id")

    return render(request, "client/index.html", {
        "clients": clients
    })

def liste_clients(request):
    clients = Client.objects.all().order_by('-id')

    return render(
        request,
        'clients/list.html',
        {
            'clients': clients
        }
    )




def detail_client(request, id):
    client = get_object_or_404(Client, id=id)
    return render(request, "clients/detail.html", {
        "client": client
    })

def edit_client(request, id):
    client = get_object_or_404(Client, id=id)

    if request.method == "POST":
        client.nom = request.POST.get("nom")
        client.telephone = request.POST.get("telephone")
        client.email = request.POST.get("email")
        client.adresse = request.POST.get("adresse")
        client.save()
        messages.success(request, "Client modifié avec succès ✅")
        return redirect("liste_clients")  # IMPORTANT

    return render(request, "clients/edit.html", {
        "client": client
    })

def delete_client(request, id):
    client = get_object_or_404(Client, id=id)
    client.delete()
    return redirect('liste_clients')
