# Generated by Django 5.0.1 on 2024-03-09 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GroceryApp', '0002_rename_pet_image_grocery_grocery_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='grocery',
            name='unit',
            field=models.CharField(default='1-kg', max_length=50),
        ),
    ]
