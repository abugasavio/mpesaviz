# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('code', models.CharField(max_length=30)),
                ('date', models.DateTimeField()),
                ('type', models.CharField(default=b'sent', max_length=20, choices=[(b'sent', b'Sent Transactions'), (b'received', b'Received Transactions'), (b'paybill', b'Pay bill Transactions'), (b'buy_good', b'Buy Good Transactions'), (b'airtime', b'Airtime'), (b'deposits', b'Deposits'), (b'withdrawals', b'Withdrawals')])),
                ('amount', models.DecimalField(max_digits=10, decimal_places=4)),
                ('recipient', models.CharField(max_length=30, blank=True)),
                ('sent_by', models.CharField(max_length=30, blank=True)),
                ('account_number', models.CharField(max_length=30)),
                ('airtime_for', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
