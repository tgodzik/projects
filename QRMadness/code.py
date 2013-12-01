from qrtools import QR

myCode = QR(data=u"Name : Tomasz; Surname : Godzik ")

myCode.encode(filename="result.png")
print myCode.filename