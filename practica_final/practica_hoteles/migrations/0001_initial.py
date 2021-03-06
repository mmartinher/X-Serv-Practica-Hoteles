# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-17 11:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha', models.DateField(auto_now=True)),
                ('comentario', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=50, null=True)),
                ('color', models.CharField(blank=True, max_length=10, null=True)),
                ('medida', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Fav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('pagina', models.TextField()),
                ('direccion', models.CharField(max_length=100)),
                ('categoria', models.CharField(max_length=30)),
                ('estrellas', models.CharField(max_length=30)),
                ('descripcion', models.TextField()),
                ('latitud', models.FloatField(default=0.0)),
                ('longitud', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('hotel', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='practica_hoteles.Hotel')),
            ],
        ),
        migrations.AddField(
            model_name='fav',
            name='hotel',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='practica_hoteles.Hotel'),
        ),
        migrations.AddField(
            model_name='fav',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comentario',
            name='hotel',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='practica_hoteles.Hotel'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
