# Generated by Django 5.0 on 2023-12-06 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_ver_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ver_code',
            field=models.CharField(default='750816212374', max_length=15, verbose_name='Проверочный код'),
        ),
    ]
