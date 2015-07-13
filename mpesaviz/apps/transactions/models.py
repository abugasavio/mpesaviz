from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField


class Transaction(TimeStampedModel):
    TYPES = Choices(('sent', 'Sent Transactions'), ('received', 'Received Transactions'), ('paybill', 'Pay bill Transactions'),
                    ('buy_good', 'Buy Good Transactions'), ('airtime', 'Airtime'), ('deposits', 'Deposits'), ('withdrawals', 'Withdrawals'),)

    code = models.CharField(max_length=30)
    date = models.DateTimeField()
    type = models.CharField(choices=TYPES, max_length=20, default=TYPES.sent)
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    recipient = models.CharField(max_length=30, blank=True)
    phonenumber = PhoneNumberField()
    sent_by = models.CharField(max_length=30, blank=True)
    account_number = models.CharField(max_length=30)
    airtime_for = models.CharField(max_length=30)


class UploadFile(TimeStampedModel):
    type = models.CharField(choices=Transaction.TYPES, max_length=20, default=Transaction.TYPES.sent)
    file = models.FileField(upload_to='uploads/')
