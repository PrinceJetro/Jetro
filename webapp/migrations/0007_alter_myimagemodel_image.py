# Generated by Django 4.1.7 on 2023-04-17 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_myimagemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myimagemodel',
            name='image',
            field=models.ImageField(upload_to='tmp/'),
        ),
    ]
