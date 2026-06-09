from django.db import models
from django.contrib.auth.models import User


# =========================
# 👤 CLIENT
# =========================
class Client(models.Model):
    nom = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom


# =========================
# 🏗️ PROJET
# =========================
class Projet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    localisation = models.CharField(max_length=255)
    date_debut = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nom


# =========================
# 📦 MATÉRIAUX
# =========================
class Materiau(models.Model):
    designation = models.CharField(max_length=200)
    unite = models.CharField(max_length=20)
    prix_unitaire = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.designation


# =========================
# 📄 DEVIS
# =========================
class Devis(models.Model):

    STATUT_CHOICES = [
        ("brouillon", "Brouillon"),
        ("envoye", "Envoyé"),
        ("accepte", "Accepté"),
        ("refuse", "Refusé"),
    ]

    numero = models.CharField(max_length=50, unique=True)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="devis")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="brouillon")
    date_creation = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(l.total() for l in self.lignes.all())

    def __str__(self):
        return self.numero


# =========================
# 📄 LIGNES DEVIS
# =========================
class LigneDevis(models.Model):
    devis = models.ForeignKey(Devis, on_delete=models.CASCADE, related_name="lignes")
    materiau = models.ForeignKey(Materiau, on_delete=models.CASCADE)

    quantite = models.DecimalField(max_digits=12, decimal_places=2)
    prix_unitaire = models.DecimalField(max_digits=12, decimal_places=2)

    def total(self):
        return self.quantite * self.prix_unitaire


# =========================
# ⚙️ PARAMÈTRES SYSTÈME
# =========================
class SystemSettings(models.Model):
    nom_entreprise = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logo/', null=True, blank=True)
    devise = models.CharField(max_length=10, default="FCFA")

    def __str__(self):
        return self.nom_entreprise


# =========================
# 👤 PROFIL UTILISATEUR
# =========================
class Profil(models.Model):

    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("agent", "Agent"),
        ("commercial", "Commercial"),
        ("conducteur", "Conducteur"),
        ("responsable", "Responsable"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="agent")

    def __str__(self):
        return f"{self.user.username} - {self.role}"