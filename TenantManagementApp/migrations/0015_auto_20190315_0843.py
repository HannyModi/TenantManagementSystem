# Generated by Django 2.1.7 on 2019-03-15 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TenantManagementApp', '0014_auto_20190315_0505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblrentcollection',
            name='rc_property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TenantManagementApp.TblPropertyAllocation'),
        ),
    ]
