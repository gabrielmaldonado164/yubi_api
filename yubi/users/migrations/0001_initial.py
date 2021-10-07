# Generated by Django 3.2.6 on 2021-10-06 01:01

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('date_modified', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de modificacion')),
                ('email', models.EmailField(error_messages={'unique': 'A user with that email alredy exists'}, max_length=254, unique=True, verbose_name='Email addres')),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message='Phone numbrer must be entered in the format: +9999999999. Up to 15 digits allowed', regex='\\+?1?\\d{9,15}$')], verbose_name='Numero telefonico')),
                ('is_client', models.BooleanField(default=False, help_text='Help easily disinguish users and perform queries.Clients are the main type of user', verbose_name='Estado Cliente')),
                ('is_verified', models.BooleanField(default=False, help_text='Set to true when the user have verified its email addres.', verbose_name='Verificacion de email')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_creation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_create_for', to=settings.AUTH_USER_MODEL, verbose_name='Usuario creador')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
                ('user_update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_update_for', to=settings.AUTH_USER_MODEL, verbose_name='Usuario modificacor')),
            ],
            options={
                'ordering': ['-date_created', '-date_modified'],
                'get_latest_by': 'date_created',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('date_modified', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de modificacion')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='users/pictures/', verbose_name='Imagen')),
                ('biography', models.TextField(blank=True, max_length=500, verbose_name='Biografia')),
                ('rides_taken', models.PositiveBigIntegerField(default=0, verbose_name='Viajes tomados')),
                ('rides_offered', models.PositiveBigIntegerField(default=0, verbose_name='Viajes ofrecidos')),
                ('reputation', models.FloatField(default=0.0, verbose_name='Reputacion')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_creation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_create_for', to=settings.AUTH_USER_MODEL, verbose_name='Usuario creador')),
                ('user_update', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_update_for', to=settings.AUTH_USER_MODEL, verbose_name='Usuario modificacor')),
            ],
            options={
                'ordering': ['-date_created', '-date_modified'],
                'get_latest_by': 'date_created',
                'abstract': False,
            },
        ),
    ]
