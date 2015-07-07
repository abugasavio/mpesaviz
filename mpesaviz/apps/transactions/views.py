from smartmin.views import SmartCRUDL, SmartListView
from .models import Transaction


class TransactionCRUDL(SmartCRUDL):
    permissions = False
    model = Transaction
