# Generated by Django 3.2.8 on 2021-10-28 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('food_name', models.CharField(max_length=500)),
            ],
            options={
                'ordering': ['-time'],
            },
        ),
    ]
