from converter import ImageMessage, convert, TextMessage
from PIL import Image

img = Image.open('test.png')
msg = ImageMessage(img)
print(msg.data)

msg = TextMessage("12345123451234512")
print(msg.data)
print(msg.len)

#print(convert([TextMessage("Hello")]))
