# Generated by Django 2.0.7 on 2018-07-05 20:41

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('density', '0002_auto_20180705_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doorway_DPU_Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('behind_space', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='behind_spaces', to='density.Space')),
                ('doorway', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dpus', to='density.Doorway')),
                ('dpu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doorways', to='density.DPU')),
                ('facing_space', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='facing_spaces', to='density.Space')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
