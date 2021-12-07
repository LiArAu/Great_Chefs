# Generated by Django 3.2.9 on 2021-12-07 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chefapp', '0003_alter_recipecontent_publisher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipecontent',
            name='publisher',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='zone_created',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='InviteLink',
        ),
    ]