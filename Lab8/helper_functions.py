from datetime import datetime
from PyQt5 import QtCore

def qt_date_to_python_datetime(qt_datetime: QtCore.QDate) -> datetime:
    return datetime.fromisoformat(qt_datetime.toString("yyyy-MM-ddTHH:mm:ss"))