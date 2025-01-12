# Generated by Django 3.1.14 on 2025-01-12 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0006_auto_20250111_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='evolved_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evolves_to', to='pokemon_entities.pokemon', verbose_name='Из кого эволюционировал'),
        ),
    ]