from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suscriber', '0002_auto_20190623_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
