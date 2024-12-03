# Generated by Django 5.1.2 on 2024-11-21 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0004_alter_planningpaiements_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='date_debut',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='credit',
            name='date_fin',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='credit',
            name='statut',
            field=models.CharField(choices=[('en cours', 'En cours'), ('payé', 'Payé'), ('retard', 'En retard')], db_index=True, default='en cours', max_length=10),
        ),
    ]
