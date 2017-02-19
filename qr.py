import qrcode

def generateQRImage(data):
    image = qrcode.make(data)
    return image
