from django.test import TestCase
import os
import sys
import django
from datetime import date
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Project.settings")
django.setup()

from credit.models import Credit, Client

# try:
#     client = Client.objects.get(id=1)

#     nouveau_credit = Credit(
#         client=client,
#         montant_total=Decimal("1000000.00"),
#         taux_interet=Decimal("4.5"),
#         duree_mois=12,
#         date_debut=date.today(),
#     )
#     nouveau_credit.save()
#     print(f"Crédit enregistré avec succès : {nouveau_credit}")

# except Client.DoesNotExist:
#     print("Le client avec l'ID 1 n'existe pas. Veuillez vérifier vos données.")
# except Exception as e:
#     print(f"Une erreur s'est produite : {e}")


# credits = Credit.objects.all()
# for credit in credits:
#     paiements_total = credit.paiements.aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0
#     credit.montant_restant = max(credit.montant_total - paiements_total, 0)
#     if credit.montant_restant == 0:
#         credit.statut = 'payé'
#     credit.save()
# print("Montant restant recalculé pour tous les crédits.")

