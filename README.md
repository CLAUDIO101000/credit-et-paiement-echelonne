# Crédit et Paiement Échelonné

## 📄 Description

Le projet **Crédit et Paiement Échelonné** est une application Django permettant de gérer les crédits accordés aux clients et leurs paiements de manière échelonnée. Ce système permet de suivre l'état des crédits, les échéances de paiement, et d'assurer une gestion claire et efficace des garanties associées aux crédits.

## ✨ Fonctionnalités

### Gestion des Clients
- Enregistrement des informations personnelles des clients : nom, prénom, adresse, téléphone, email, date de naissance.
- Chaque client peut avoir plusieurs crédits associés.

### Gestion des Crédits
- Calcul automatique du montant total du crédit avec le taux d'intérêt.
- Suivi du statut du crédit : **En cours**, **Payé**, **En retard**.
- Gestion de la durée du crédit et des montants restants à payer.

### Gestion des Plannings d’Échéances
- Création d’échéances de paiement pour chaque crédit.
- Suivi du statut des échéances : **En attente**, **Payé**, **En retard**.
- Validation des montants des échéances en fonction des paiements restants.

### Gestion des Paiements
- Enregistrement des paiements avec différents modes : chèque, carte bancaire, espèces, virement bancaire.
- Mise à jour automatique des statuts des échéances et crédits après chaque paiement.

### Gestion des Garanties
- Association de garanties aux crédits : hypothèque, nantissement, caution, autre.
- Suivi du statut des garanties : **Active**, **Utilisée**, **Expirée**.
- Stockage des descriptions et des valeurs estimées des garanties.

## 🛠️ Modèles de Données

### Client
- **Champs** : nom, prénom, adresse, téléphone, email, date_naissance.
- **Méthodes principales** :
  - `__str__()` : Retourne le nom complet du client.

### Crédit
- **Champs** : client, montant_credit, montant_total, montant_restant, taux_interet, duree_mois, date_debut, date_fin, statut.
- **Statuts possibles** : en cours, payé, retard.
- **Méthodes principales** :
  - `calculer_montant_total()` : Calcule le montant total à payer.
  - `calculer_montant_restant()` : Calcule le montant restant à payer.
  - `update_credit_status()` : Met à jour le statut du crédit en fonction des paiements effectués.

### PlanningPaiements
- **Champs** : credit, numero_echeance, montant_echeance, date_echeance, statut.
- **Statuts possibles** : payé, attente, retard.
- **Méthodes principales** :
  - `update_statut_et_montant()` : Met à jour le statut et le montant restant d'une échéance.

### Paiement
- **Champs** : credit, planning, montant_paye, date_paiement, mode_paiement.
- **Modes de paiement** : chèque, carte, espèces, virement.
- **Méthodes principales** :
  - `save()` : Gère la validation des paiements et met à jour les statuts liés.

### Garantie
- **Champs** : credit, type_garantie, valeur_estimee, description, statut.
- **Statuts possibles** : active, utilisée, expirée.

## ⚙️ Prérequis

- Python 3.8+
- Django 4.0+
- Bibliothèques Python additionnelles : `dateutil`, `mysqlclient` (ou tout autre connecteur compatible avec votre base de données).

## 🚀 Installation

### Cloner le dépôt

```bash
git clone https://github.com/votre-repo/credit-et-paiement-echelonne.git
cd credit-et-paiement-echelonne
```

### Créer un environnement virtuel et l'activer

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

### Appliquer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Lancer le serveur
```bash
python manage.py runserver
```

### 🌐 Utilisation
Accédez à l'interface utilisateur via http://127.0.0.1:8000.
Utilisez l'interface pour gérer les clients, crédits, paiements et garanties.

## 👤 Auteur
- **Nom de l'auteur** : RANAIVOSON Nantenaina Claudio
- **e-mail** : ranaivosonclaudio@gmail.com
- **tel** : 032 43 372 46
