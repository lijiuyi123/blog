# Generated by Django 2.0.2 on 2018-03-02 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-changed_time'], 'verbose_name_plural': '博客'},
        ),
    ]
