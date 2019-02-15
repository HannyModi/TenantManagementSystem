# Generated by Django 2.1.5 on 2019-02-15 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TenantManagementApp', '0004_tblmasterpropertyclone_cln_is_master_clone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tblmasterproperty',
            name='msp_is_allocated',
        ),
        migrations.AddField(
            model_name='tblmasterpropertyclone',
            name='cln_is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tblmasterpropertyclone',
            name='cln_is_allocated',
            field=models.BooleanField(default=False),
        ),
    ]
