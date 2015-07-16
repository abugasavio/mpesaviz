from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from django_pandas.io import read_frame


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

    def monthly_transactions(self):
        dataframe = read_frame(Transaction.objects.all())
        dataframe['month'] = [date.strftime('%B') for date in dataframe['date']]
        dataframe['year'] = [date.strftime('%Y') for date in dataframe['date']]
        groups = dataframe.groupby(['year', 'month', 'type'])['amount'].sum().reset_index(name='amount')
        return groups

    def top_recipients(self):
        dataframe = read_frame(Transaction.objects.all())
        recipient_dataframe = dataframe[dataframe.type == 'Sent Transactions']
        return recipient_dataframe.groupby(['recipient', 'type'])['amount'].sum().reset_index(name='amount').sort('amount', ascending=False)




class UploadFile(TimeStampedModel):
    type = models.CharField(choices=Transaction.TYPES, max_length=20, default=Transaction.TYPES.sent)
    file = models.FileField(upload_to='uploads/')
