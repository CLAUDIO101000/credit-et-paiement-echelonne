# Generated by Django 5.1.2 on 2024-11-26 14:49

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0008_garantie_statut_alter_credit_montant_restant'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='garantie',
            options={'ordering': ['credit', 'type_garantie'], 'verbose_name': 'Garantie', 'verbose_name_plural': 'Garanties'},
        ),
        migrations.AddField(
            model_name='garantie',
            name='date_creation',
            field=models.DateField(auto_now_add=True, default=datetime.date(2024, 11, 26), verbose_name='Date de création'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='credit',
            name='montant_credit',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='credit',
            name='montant_restant',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='credit',
            name='montant_total',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='garantie',
            name='credit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='garanties', to='credit.credit', verbose_name='Crédit associé'),
        ),
        migrations.AlterField(
            model_name='garantie',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description de la garantie'),
        ),
        migrations.AlterField(
            model_name='garantie',
            name='statut',
            field=models.CharField(choices=[('active', 'Active'), ('utilisée', 'Utilisée'), ('expirée', 'Expirée')], default='active', max_length=20, verbose_name='Statut de la garantie'),
        ),
        migrations.AlterField(
            model_name='garantie',
            name='type_garantie',
            field=models.CharField(choices=[('hypotheque', 'Hypothèque'), ('nantissement', 'Nantissement'), ('caution', 'Caution'), ('autre', 'Autre')], max_length=50, verbose_name='Type de garantie'),
        ),
        migrations.AlterField(
            model_name='garantie',
            name='valeur_estimee',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Valeur estimée'),
        ),
        migrations.AlterField(
            model_name='paiement',
            name='montant_paye',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name='planningpaiements',
            name='montant_echeance',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]
