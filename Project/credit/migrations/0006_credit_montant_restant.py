# Generated by Django 5.1.2 on 2024-11-25 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0005_alter_credit_date_debut_alter_credit_date_fin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='credit',
            name='montant_restant',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10),
        ),
    ]
