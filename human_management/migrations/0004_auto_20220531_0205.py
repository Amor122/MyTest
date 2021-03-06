# Generated by Django 3.2.13 on 2022-05-30 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('human_management', '0003_alter_organizationtype_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='organization_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='down_organization', to='human_management.organizationtype', verbose_name='组织类型'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='up_organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='down_organization', to='human_management.organization', verbose_name='上级组织'),
        ),
    ]
