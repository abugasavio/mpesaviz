from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel


class Transaction(TimeStampedModel):
    TYPES = Choices(('sent', 'Sent Transactions'), ('received', 'Received Transactions'), ('paybill', 'Pay bill Transactions'),
                    ('buy_good', 'Buy Good Transactions'), ('airtime', 'Airtime'), ('deposits', 'Deposits'), ('withdrawals', 'Withdrawals'),)

    code = models.CharField(max_length=30)
    date = models.DateTimeField()
    type = models.CharField(choices=TYPES, max_length=20, default=TYPES.sent)
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    recipient = models.CharField(max_length=30, blank=True)
    sent_by = models.CharField(max_length=30, blank=True)
    account_number = models.CharField(max_length=30)
    airtime_for = models.CharField(max_length=30)
