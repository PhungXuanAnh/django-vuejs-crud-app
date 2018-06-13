# Generated by Django 2.0.6 on 2018-06-13 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(help_text='Enter Stock Keeping Unit', max_length=13)),
                ('name', models.CharField(help_text='Enter product name', max_length=200)),
                ('description', models.TextField(help_text='Enter product description')),
                ('buyPrice', models.DecimalField(decimal_places=2, help_text='Enter product price per unit', max_digits=20)),
                ('sellPrice', models.DecimalField(decimal_places=2, help_text='Enter product price per unit', max_digits=20)),
                ('unit', models.CharField(help_text='Enter product unit', max_length=10)),
                ('quantity', models.DecimalField(decimal_places=1, help_text='Enter quantity', max_digits=20)),
            ],
        ),
    ]
