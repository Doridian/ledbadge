from converter import ImageMessage, convert, TextMessage, Mode
from bluetooth import send
from PIL import Image

img = Image.open('test.png')
# SNOWFLAKE is basically instant display. WARNING: All "pages" after 1 skip the first 4 rows.
# So it displays like this [44 pixels] [4 pixels invisible] [44 pixels]
# Make sure to take this into account when creating animations using SNOWFLAKE (see test.png provided)
msg = ImageMessage(img, speed=0x3, mode=Mode.SNOWFLAKE)

#msg = TextMessage('123451234512345', mode=Mode.SNOWFLAKE)

data = convert([
        msg
])

print(data)

send("xx:xx:xx:xx:xx:xx", data)
