# Generated by Django 4.2 on 2025-01-20 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasketModl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('count', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='storeapp.userprofile')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='storeapp.tovarmodel')),
            ],
        ),
    ]
