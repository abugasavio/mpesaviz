import csv
import time
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from smartmin.views import SmartCRUDL, SmartFormView, SmartListView
from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers.phonenumberutil import NumberParseException
from .models import Transaction
from .forms import UploadFileForm


class GraphDataView(View):
    def get(self, request, *args, **kwargs):
        data_type = request.GET.get('type')

        if data_type == 'all_time_sent_vs_received':
            data = [{'name': 'Sent', 'data': [166342]}, {'name': 'Received', 'data': [429847]}]

        elif data_type == 'top_recipients':
            top_recipients = Transaction().top_recipients()
            data = [{
                'name': 'Recipient',
                'data': [row['recipient'] for index, row in top_recipients.iterrows()]
            }, {
                'name': 'Amounts',
                'data': [int(row['amount']) for index, row in top_recipients.iterrows()]
            }]
        else:
            groups = Transaction().monthly_transactions()
            received_2015 = groups[(groups.year == '2015') & (groups.type == 'Received Transactions')]
            sent_2015 = groups[(groups.year == '2015') & (groups.type == 'Sent Transactions')]

            data = [{'name': 'Sent', 'data': [int(sent_2015[sent_2015.month == 'January'].amount),
                                              int(sent_2015[sent_2015.month == 'February'].amount),
                                              int(sent_2015[sent_2015.month == 'March'].amount),
                                              int(sent_2015[sent_2015.month == 'April'].amount),
                                              int(sent_2015[sent_2015.month == 'May'].amount),
                                              int(sent_2015[sent_2015.month == 'June'].amount)]
                     }, {'name': 'Received', 'data': [int(received_2015[received_2015.month == 'January'].amount),
                                                      int(received_2015[received_2015.month == 'February'].amount),
                                                      int(received_2015[received_2015.month == 'March'].amount),
                                                      int(received_2015[received_2015.month == 'April'].amount),
                                                      int(received_2015[received_2015.month == 'May'].amount),
                                                      0]
                         }
                    ]
        return JsonResponse(data, safe=False)


class TransactionCRUDL(SmartCRUDL):
    permissions = False
    model = Transaction
    actions = ('read', 'update', 'list', 'upload')

    class List(SmartListView):
        fields = ('id', 'code', 'date', 'type', 'amount', 'recipient', 'phonenumber')
        default_order = '-date'

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

                # received transactions
                if file_type == Transaction.TYPES.received:
                    try:
                        date = time.strptime(transaction['Date'], '%d/%m/%Y %H:%M:%S')
                        date = datetime(*date[:6])
                        transactions.append(Transaction(code=transaction['\xef\xbb\xbf"Code"'], date=date, sent_by=transaction['Sent By'],
                                                        amount=float(transaction['Amount'].replace(",", "")), type=file_type))
                    except NumberParseException:
                        pass

            Transaction.objects.bulk_create(transactions)



