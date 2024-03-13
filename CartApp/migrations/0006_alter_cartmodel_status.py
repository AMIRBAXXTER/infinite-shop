# Generated by Django 5.0.2 on 2024-03-13 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CartApp', '0005_cartmodel_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartmodel',
            name='status',
            field=models.CharField(choices=[('در انتظار پرداخت', 'در انتظار پرداخت'), ('پرداخت شده', 'پرداخت شده'), ('ارسال شده', 'ارسال شده'), ('تکمیل شده', 'تکمیل شده')], default='در انتظار پرداخت', max_length=25, verbose_name='وضعیت'),
        ),
    ]
