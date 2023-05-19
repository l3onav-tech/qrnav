import qrcode
qr = qrcode.QRCode(
    version=2,
    box_size=50,
    border=1
)
qr.add_data("https://api.qrnav.tech/v1/user/8de0634-1d90-4fa7-9288-74a0d6219b47")
qr.make(fit=True)
img = qr.make_image(fill='black', back_color='white')
print(img)

