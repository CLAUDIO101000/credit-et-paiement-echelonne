from django.db import models
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import date
from django.db.models import Sum
from django.db import transaction

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    date_naissance = models.DateField()

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Credit(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name="credits")
    montant_credit = models.DecimalField(max_digits=15, decimal_places=2)
    montant_total = models.DecimalField(max_digits=15, decimal_places=2)
    montant_restant = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    taux_interet = models.DecimalField(max_digits=5, decimal_places=2)
    duree_mois = models.IntegerField()
    date_debut = models.DateField(db_index=True)
    date_fin = models.DateField(blank=True, null=True)
    
    STATUT_CHOICES = [
        ('en cours', 'En cours'),
        ('payé', 'Payé'),
        ('retard', 'En retard'),
    ]
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='en cours', db_index=True)

    def clean(self):
        super().clean()
        if self.date_debut > date.today():
            raise ValidationError({'date_debut': "La date de début ne peut pas être dans le futur."})
        if self.date_fin and self.date_fin < self.date_debut:
            raise ValidationError({'date_fin': "La date de fin ne peut pas être avant la date de début."})
        if self.duree_mois <= 0:
            raise ValidationError({'duree_mois': "La durée du crédit doit être un nombre positif."})
        if self.montant_credit <= 0:
            raise ValidationError({'montant_credit': "Le montant du crédit doit être positif."})
        if self.taux_interet <= 0 or self.taux_interet > 100:
            raise ValidationError({'taux_interet': "Le taux d'intérêt doit être compris entre 0 et 100."})

    def calculer_montant_total(self):
        return self.montant_credit * (1 + (self.taux_interet / 100))

    def calculer_montant_restant(self):
        paiements_total = self.paiements.aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0
        montant_restant = max(self.montant_total - paiements_total, 0)
        return montant_restant

    def update_credit_status(self, force_save=False):
        self.montant_restant = self.calculer_montant_restant()
        today = date.today()
        if today > self.date_fin and self.montant_restant > 0:
            self.statut = 'retard'
        elif self.montant_restant == 0:
            self.statut = 'payé'
        else:
            self.statut = 'en cours'
        if force_save:
            self.save()

    def save(self, *args, **kwargs):
        if self.date_debut and self.duree_mois > 0:
            self.date_fin = self.date_debut + relativedelta(months=self.duree_mois)
        if self.montant_credit > 0 and self.taux_interet > 0:
            self.montant_total = self.calculer_montant_total()
        if not self.pk:
            super().save(*args, **kwargs)
        self.update_credit_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Crédit {self.id} - Client {self.client.nom} {self.client.prenom}"

class PlanningPaiements(models.Model):
    id = models.AutoField(primary_key=True)
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name="plannings")
    numero_echeance = models.IntegerField()
    montant_echeance = models.DecimalField(max_digits=15, decimal_places=2)
    date_echeance = models.DateField()
    STATUT_CHOICES = [
        ('payé', 'Payé'),
        ('attente', 'En attente'),
        ('retard', 'En retard'),
    ]
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='attente')

    class Meta:
        unique_together = ('credit', 'numero_echeance')

    def clean(self):
        if self.numero_echeance <= 0:
            raise ValidationError({'numero_echeance': "Le numero de l'échéance doit être positif."})
        if self.montant_echeance <= 0:
            raise ValidationError({'montant_echeance': "Le montant de l'échéance doit être positif."})
        if not self.credit.date_debut <= self.date_echeance <= self.credit.date_fin:
            raise ValidationError({
                'date_echeance': f"La date d'échéance doit être comprise entre la date de début "
                                 f"({self.credit.date_debut.strftime('%d/%m/%Y')}) et la date de fin ({self.credit.date_fin.strftime('%d/%m/%Y')})."
            })
        montant_echeance_precedent = 0
        if self.pk:
            montant_echeance_precedent = type(self).objects.get(pk=self.pk).montant_echeance
            total_echeances_existantes = self.credit.plannings.exclude(pk=self.pk).aggregate(
                total=Sum('montant_echeance')
            )['total'] or 0
        montant_restant = self.credit.montant_restant - total_echeances_existantes
        if self.montant_echeance > montant_restant:
            montant_restant_formate = f"{montant_restant:,.0f}".replace(',', ' ') + " Ar"
            montant_echeance_formate = f"{self.montant_echeance:,.0f}".replace(',', ' ') + " Ar"
            raise ValidationError({
                'montant_echeance': f"Le montant d'échéance ({montant_echeance_formate}) "
                                    f"ne peut pas dépasser le montant restant du crédit ({montant_restant_formate})."
            })
        super().clean()

    def update_statut_et_montant(self):
        paiements_total = self.paiements.aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0
        self.montant_restant = max(self.montant_echeance - paiements_total, 0)
        if self.montant_restant == 0:
            self.statut = 'payé'
        elif date.today() > self.date_echeance and self.montant_restant > 0:
            self.statut = 'retard'
        else:
            self.statut = 'attente'
        self.save()

    def __str__(self):
        return f"Planning {self.numero_echeance} - Crédit {self.credit.id}"

class Paiement(models.Model):
    id = models.AutoField(primary_key=True)
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name="paiements")
    planning = models.ForeignKey(PlanningPaiements, on_delete=models.CASCADE, related_name="paiements")
    montant_paye = models.DecimalField(max_digits=15, decimal_places=2)
    date_paiement = models.DateField()
    mode_paiement = models.CharField(max_length=10, choices=[
        ('cheque', 'Chèque'),
        ('carte', 'Carte bancaire'),
        ('espece', 'Espèces'),
        ('virement', 'Virement bancaire'),
    ])

    def clean(self):
        if self.montant_paye <= 0:
            raise ValidationError({'montant_paye': "Le montant payé doit être positif."})
        if self.planning.credit != self.credit:
            raise ValidationError({
                'credit': f"Le crédit {self.credit.id} n'est pas associé au planning {self.planning.numero_echeance} du crédit {self.planning.credit.id}."
            })
        if self.montant_paye <= 0:
            raise ValidationError({
                'montant_paye': "Le montant payé doit être positif."
            })
        if not (self.credit.date_debut <= self.date_paiement <= self.planning.date_echeance):
            raise ValidationError({
                'date_paiement': f"La date de paiement doit être comprise entre la date de début du crédit "
                                 f"({self.credit.date_debut.strftime('%d/%m/%Y')}) et la date d'échéance du planning ({self.planning.date_echeance.strftime('%d/%m/%Y')})."
            })
        montant_paye_precedent = 0
        if self.pk:
            montant_paye_precedent = type(self).objects.get(pk=self.pk).montant_paye
        total_paiements_existants = self.planning.paiements.exclude(pk=self.pk).aggregate(
            total=Sum('montant_paye')
        )['total'] or 0
        total_paiements_actuels = total_paiements_existants + self.montant_paye
        if total_paiements_actuels > self.planning.montant_echeance:
            montant_echeance_formate = f"{self.planning.montant_echeance:,.0f}".replace(',', ' ') + " Ar"
            total_paiements_formate = f"{total_paiements_actuels:,.0f}".replace(',', ' ') + " Ar"
            raise ValidationError({
                'montant_paye': f"Le total des paiements pour ce planning ({total_paiements_formate}) "
                                f"ne peut pas dépasser le montant de l'échéance ({montant_echeance_formate})."
            })
        super().clean()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            super().delete(*args, **kwargs)
            if self.planning:
                self.planning.update_statut_et_montant()
            if self.credit:
                self.credit.update_credit_status()
                self.credit.update_credit_status(force_save=True)

    def save(self, *args, **kwargs):
        if self.pk:
            paiement_precedent = Paiement.objects.get(pk=self.pk)
            changements = []
            if paiement_precedent.montant_paye != self.montant_paye:
                changements.append(f"Montant payé modifié : {paiement_precedent.montant_paye} -> {self.montant_paye}")
            if paiement_precedent.date_paiement != self.date_paiement:
                changements.append(f"Date de paiement modifiée : {paiement_precedent.date_paiement} -> {self.date_paiement}")
            if paiement_precedent.mode_paiement != self.mode_paiement:
                changements.append(f"Mode de paiement modifié : {paiement_precedent.mode_paiement} -> {self.mode_paiement}")
            if changements:
                HistoriquePaiement.objects.create(
                    paiement=self,
                    remarque="<br>".join(changements)
                )
        super().save(*args, **kwargs)
        if self.planning:
            self.planning.update_statut_et_montant()
        if self.credit:
            self.credit.update_credit_status()
            self.credit.update_credit_status(force_save=True)
            
    def __str__(self):
        return f"Paiement {self.id} - Crédit {self.credit.id}"

class Garantie(models.Model):
    id = models.AutoField(primary_key=True)
    credit = models.ForeignKey('Credit', on_delete=models.CASCADE, related_name="garanties", verbose_name="Crédit associé")
    type_garantie = models.CharField(max_length=50,
        choices=[
            ('hypotheque', 'Hypothèque'),
            ('nantissement', 'Nantissement'),
            ('caution', 'Caution'),
            ('autre', 'Autre'),
        ],
        verbose_name="Type de garantie")
    valeur_estimee = models.DecimalField( max_digits=15, decimal_places=2, verbose_name="Valeur estimée")
    description = models.TextField(blank=True, verbose_name="Description de la garantie")
    statut = models.CharField(max_length=20, 
        choices=[
            ('active', 'Active'),
            ('utilisée', 'Utilisée'),
            ('expirée', 'Expirée'),
        ], 
        default='active', verbose_name="Statut de la garantie")
    date_creation = models.DateField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Garantie"
        verbose_name_plural = "Garanties"
        ordering = ['credit', 'type_garantie']

    def __str__(self):
        return f"Garantie {self.type_garantie} - Crédit {self.credit}"

    def clean(self):
        if self.valeur_estimee <= 0:
            raise ValidationError({'valeur_estimee': "La valeur estimée doit être positive."})

class HistoriquePaiement(models.Model):
    id = models.AutoField(primary_key=True)
    paiement = models.ForeignKey(Paiement, on_delete=models.CASCADE, related_name="historiques")
    date_modification = models.DateTimeField(auto_now=True)
    remarque = models.TextField(blank=True)

    def __str__(self):
        return f"Historique - Paiement {self.paiement.id} - {self.date_modification}"
