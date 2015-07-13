import csv
import time
from datetime import datetime
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from smartmin.views import SmartCRUDL, SmartFormView
from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers.phonenumberutil import NumberParseException
from .models import Transaction
from .forms import UploadFileForm



class TransactionCRUDL(SmartCRUDL):
    permissions = False
    model = Transaction
    actions = ('read', 'update', 'list', 'upload')

    class Upload(SmartFormView):
        form_class = UploadFileForm

        def form_valid(self, form):
            file_type = form.cleaned_data.get('type')
            self.update_records(self.request.FILES['file'], file_type)
            return redirect(reverse('transactions.transaction_list'))

        def update_records(self, uploaded_file, file_type):
            transactions = []
            for transaction in csv.DictReader(uploaded_file, delimiter=',',):

                # sent transactions
                if file_type == Transaction.TYPES.sent:
                    try:
                        date = time.strptime(transaction['Date'], '%d/%m/%Y %H:%M:%S')
                        date = datetime(*date[:6])
                        transactions.append(Transaction(code=transaction['Code'], date=date, recipient=transaction['Recipient'],
                                                        amount=float(transaction['Amount'].replace(",", "")), type=file_type, phonenumber=PhoneNumber.from_string(transaction['No.'], 'KE')))
                    except NumberParseException:
                        pass
            Transaction.objects.bulk_create(transactions)



