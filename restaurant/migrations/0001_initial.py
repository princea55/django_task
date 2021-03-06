# Generated by Django 3.1.2 on 2020-10-09 03:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foodName', models.CharField(max_length=30)),
                ('price', models.CharField(max_length=20)),
                ('foodType', models.CharField(max_length=20)),
                ('noOfVariety', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('address', models.TextField()),
                ('franchise_name', models.CharField(max_length=30)),
                ('ownerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderDate', models.DateField(auto_now=True)),
                ('time', models.TimeField(auto_now=True)),
                ('tableNo', models.IntegerField()),
                ('totalBill', models.IntegerField()),
                ('FoodItemId', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant.fooditems')),
            ],
        ),
        migrations.AddField(
            model_name='fooditems',
            name='restaurantId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant'),
        ),
    ]
