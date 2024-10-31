# Generated by Django 4.0.10 on 2024-10-16 14:48

from django.conf import settings
from django.db import migrations

from swp.models.fields import DenseVectorField


class Migration(migrations.Migration):

    dependencies = [
        ('swp', '0053_convert_static_tags_to_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='embedding',
            field=DenseVectorField(dims=settings.EMBEDDING_VECTOR_DIMS, editable=False, null=True, verbose_name='embedding'),
        ),
    ]