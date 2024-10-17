# Generated by Django 4.0.10 on 2024-10-16 14:48

from django.db import migrations

from swp.models.fields import DenseVectorField


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0051_char_array_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='embedding',
            field=DenseVectorField(dims=512, editable=False, null=True, verbose_name='embedding'),
        ),
    ]
