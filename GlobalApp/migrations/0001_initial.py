# Generated by Django 3.1.7 on 2021-07-04 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('mail', models.EmailField(max_length=200)),
                ('subject', models.CharField(max_length=50)),
                ('message', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Expert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('1', 'Docteur'), ('2', 'kine'), ('3', 'nutritioniste')], max_length=20)),
                ('date_rejoin', models.DateTimeField(auto_now=True)),
                ('sexe', models.CharField(choices=[('1', 'Male'), ('2', 'Female')], max_length=10)),
                ('tel', models.CharField(max_length=100)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Infermier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=150, null=True)),
                ('mail', models.EmailField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateNaissance', models.DateTimeField()),
                ('bio', models.TextField(max_length=500)),
                ('sexe', models.CharField(choices=[('1', 'Male'), ('2', 'Female')], max_length=10)),
                ('tel', models.CharField(max_length=100)),
                ('amies', models.ManyToManyField(blank=True, related_name='_patient_amies_+', to='GlobalApp.Patient')),
                ('experts', models.ManyToManyField(to='GlobalApp.Expert')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Poste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('titre', models.CharField(max_length=10000, null=True)),
                ('contenu', models.TextField(max_length=10000)),
                ('publie_par', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GlobalApp.expert')),
            ],
        ),
        migrations.CreateModel(
            name='room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GlobalApp.infermier')),
                ('members', models.ManyToManyField(to='GlobalApp.Patient')),
                ('nomGroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
        migrations.CreateModel(
            name='publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poste_publie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GlobalApp.poste')),
                ('publie_dans', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GlobalApp.room')),
            ],
        ),
    ]
