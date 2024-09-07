# apps/users/migrations/0002_alter_customuser_birth_date_and_more.py
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birth_date',
            field=models.DateField(blank=True, null=True),  # Удаляем validators=[...]
        ),
    ]
