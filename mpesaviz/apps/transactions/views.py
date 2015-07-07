from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from smartmin.views import SmartCRUDL, SmartFormView
from .models import Transaction
from .forms import UploadFileForm



class TransactionCRUDL(SmartCRUDL):
    permissions = False
    model = Transaction
    actions = ('read', 'update', 'list', 'upload')

    class Upload(SmartFormView):
        form_class = UploadFileForm

        def form_invalid(self, form):
            assert False, form

        def form_valid(self, form):
            file_type = form.cleaned_data.get('type')
            self.update_records(self.request.FILE['file'], file_type)
            return redirect(reverse('transaction_list'))

        def update_records(self, uploaded_file, file_type):
            for chunk in uploaded_file.chunks():
                print chunk

