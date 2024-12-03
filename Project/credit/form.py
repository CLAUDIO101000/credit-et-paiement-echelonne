from django import forms
from .models import Client, Credit, PlanningPaiements, Paiement, Garantie

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'adresse', 'telephone', 'email', 'date_naissance']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Entrez le nom'}),
            'prenom': forms.TextInput(attrs={'placeholder': 'Entrez le prénom'}),
            'adresse': forms.TextInput(attrs={'placeholder': 'Entrez l\'adresse'}),
            'telephone': forms.TextInput(attrs={'placeholder': 'Entrez le numéro de téléphone'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Entrez l\'adresse email'}),
            'date_naissance': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ClientUpForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'adresse', 'telephone', 'email', 'date_naissance']
        widgets = {
            'date_naissance': forms.TextInput(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = ['client','montant_credit', 'taux_interet', 'duree_mois', 'date_debut']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'montant_credit': forms.NumberInput(attrs={'placeholder': 'Montant du crédit'}),
            'taux_interet': forms.NumberInput(attrs={'placeholder': 'Taux d\'intérêt (%)'}),
            'duree_mois': forms.NumberInput(attrs={'placeholder': 'Durée en mois'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CreditUpForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = ['client', 'montant_credit', 'taux_interet', 'duree_mois', 'date_debut']
        widgets = {
            'date_debut': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].disabled = True
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class PlanningForm(forms.ModelForm):
    class Meta:
        model = PlanningPaiements
        fields = ['credit', 'numero_echeance', 'montant_echeance', 'date_echeance']
        widgets = {
            'credit': forms.Select(attrs={'class': 'form-control'}),
            'numero_echeance': forms.NumberInput(attrs={'placeholder': 'Numéro de l\'échéance'}),
            'montant_echeance': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Montant de l\'échéance'}),
            'date_echeance': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class PlanningUpForm(forms.ModelForm):
    class Meta:
        model = PlanningPaiements
        fields = ['credit', 'numero_echeance', 'montant_echeance', 'date_echeance']
        widgets = {
            'date_echeance': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['credit'].disabled = True
        self.fields['numero_echeance'].disabled = True
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['credit' ,'planning', 'montant_paye', 'date_paiement', 'mode_paiement']
        widgets = {
            'montant_paye': forms.NumberInput(attrs={'placeholder': 'Entrez le montant payé'}),
            'date_paiement': forms.DateInput(attrs={'type': 'date'}),
            'mode_paiement': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class PaiementUpForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['credit' ,'planning', 'montant_paye', 'date_paiement', 'mode_paiement']
        widgets = {
            'date_paiement': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['credit'].disabled = True
        self.fields['planning'].disabled = True
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class GarantieForm(forms.ModelForm):
    class Meta:
        model = Garantie
        fields = ['credit', 'type_garantie', 'valeur_estimee', 'description', 'statut']
        widgets = {
            'date_creation': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control description-field'

class GarantieUpForm(forms.ModelForm):
    class Meta:
        model = Garantie
        fields = ['credit', 'type_garantie', 'valeur_estimee', 'description', 'statut']
        widgets = {
            'date_creation': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['credit'].disabled = True
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control description-field'