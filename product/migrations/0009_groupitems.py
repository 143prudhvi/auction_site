# Generated by Django 4.2.4 on 2024-02-19 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_item_imageexist'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parentId', models.CharField(default=None, max_length=30, null=True)),
                ('childId', models.CharField(default=None, max_length=30, null=True)),
            ],
        ),
    ]
