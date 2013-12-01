# WHat about secure qr
# generate code + sumfin
from qrtools import QR

myCode = QR(filename=u"result.png")

if myCode.decode():
    print myCode.data
    print myCode.data_type
    print myCode.data_to_string()