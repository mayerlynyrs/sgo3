# Generated by Django 3.2.3 on 2022-03-10 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psicologos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacionpsicologico',
            name='tipo',
            field=models.CharField(choices=[('SUP', 'Supervisor'), ('TEC', 'Técnico')], default='TEC', max_length=3),
        ),
    ]
