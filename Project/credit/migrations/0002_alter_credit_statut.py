# Generated by Django 5.1.2 on 2024-10-27 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='statut',
            field=models.CharField(choices=[('en cours', 'En cours'), ('payé', 'Payé'), ('retard', 'En retard')], default='en cours', max_length=10),
        ),
    ]
