from enum import Enum
from binascii import unhexlify
from math import ceil

MAX_MESSAGES = 8
PACKET_START = "77616E670000"
PACKET_BYTE_SIZE = 16
PACKET_BYTE_SIZE_2 = PACKET_BYTE_SIZE * 2

CHAR_CODES = {
	'0': "007CC6CEDEF6E6C6C67C00",
	'1': "0018387818181818187E00",
	'2': "007CC6060C183060C6FE00",
	'3': "007CC606063C0606C67C00",
	'4': "000C1C3C6CCCFE0C0C1E00",
	'5': "00FEC0C0FC060606C67C00",
	'6': "007CC6C0C0FCC6C6C67C00",
	'7': "00FEC6060C183030303000",
	'8': "007CC6C6C67CC6C6C67C00",
	'9': "007CC6C6C67E0606C67C00",
	'#': "006C6CFE6C6CFE6C6C0000",
	'&': "00386C6C3876DCCCCC7600",
	'_': "00000000000000000000FF",
	'-': "0000000000FE0000000000",
	'?': "007CC6C60C181800181800",
	'@': "00003C429DA5ADB6403C00",
	'(': "000C183030303030180C00",
	')': "0030180C0C0C0C0C183000",
	'=': "0000007E00007E00000000",
	'+': "00000018187E1818000000",
	'!': "00183C3C3C181800181800",
	'\'': "1818081000000000000000",
	':': "0000001818000018180000",
	'%': "006092966C106CD2920C00",
	'/': "000002060C183060C08000",
	'"': "6666222200000000000000",
	' ': "0000000000000000000000",
	'*': "000000663CFF3C66000000",
	',': "0000000000000030301020",
	'.': "0000000000000000303000",
	'$': "107CD6D6701CD6D67C1010",
	'~': "0076DC0000000000000000",
	'[': "003C303030303030303C00",
	']': "003C0C0C0C0C0C0C0C3C00",
	'{': "000E181818701818180E00",
	'}': "00701818180E1818187000",
	'<': "00060C18306030180C0600",
	'>': "006030180C060C18306000",
	'^': "386CC60000000000000000",
	'`': "1818100800000000000000",
	';': "0000001818000018180810",
	'\\': "0080C06030180C06020000",
	'|': "0018181818001818181800",
	'a': "00000000780C7CCCCC7600",
	'b': "00E060607C666666667C00",
	'c': "000000007CC6C0C0C67C00",
	'd': "001C0C0C7CCCCCCCCC7600",
	'e': "000000007CC6FEC0C67C00",
	'f': "001C363078303030307800",
	'g': "00000076CCCCCC7C0CCC78",
	'h': "00E060606C76666666E600",
	'i': "0018180038181818183C00",
	'j': "0C0C001C0C0C0C0CCCCC78",
	'k': "00E06060666C78786CE600",
	'l': "0038181818181818183C00",
	'm': "00000000ECFED6D6D6C600",
	'n': "00000000DC666666666600",
	'o': "000000007CC6C6C6C67C00",
	'p': "000000DC6666667C6060F0",
	'q': "0000007CCCCCCC7C0C0C1E",
	'r': "00000000DE76606060F000",
	's': "000000007CC6701CC67C00",
	't': "00103030FC303030341800",
	'u': "00000000CCCCCCCCCC7600",
	'v': "00000000C6C6C66C381000",
	'w': "00000000C6D6D6D6FE6C00",
	'x': "00000000C66C38386CC600",
	'y': "000000C6C6C6C67E060CF8",
	'z': "00000000FE8C183062FE00",
	'A': "00386CC6C6FEC6C6C6C600",
	'B': "00FC6666667C666666FC00",
	'C': "007CC6C6C0C0C0C6C67C00",
	'D': "00FC66666666666666FC00",
	'E': "00FE66626878686266FE00",
	'F': "00FE66626878686060F000",
	'G': "007CC6C6C0C0CEC6C67E00",
	'H': "00C6C6C6C6FEC6C6C6C600",
	'I': "003C181818181818183C00",
	'J': "001E0C0C0C0C0CCCCC7800",
	'K': "00E6666C6C786C6C66E600",
	'L': "00F060606060606266FE00",
	'M': "0082C6EEFED6C6C6C6C600",
	'N': "0086C6E6F6DECEC6C6C600",
	'O': "007CC6C6C6C6C6C6C67C00",
	'P': "00FC6666667C606060F000",
	'Q': "007CC6C6C6C6C6D6DE7C06",
	'R': "00FC6666667C6C6666E600",
	'S': "007CC6C660380CC6C67C00",
	'T': "007E7E5A18181818183C00",
	'U': "00C6C6C6C6C6C6C6C67C00",
	'V': "00C6C6C6C6C6C66C381000",
	'W': "00C6C6C6C6D6FEEEC68200",
	'X': "00C6C66C7C387C6CC6C600",
	'Y': "00666666663C1818183C00",
	'Z': "00FEC6860C183062C6FE00"
}

BYTE_ORDER = 'little'

class Mode(Enum):
	LEFT = 0x00
	RIGHT = 0x01
	UP = 0x02
	DOWN = 0x03
	FIXED = 0x04
	SNOWFLAKE = 0x05
	PICTURE = 0x06
	ANIMATION = 0x07
	LASER = 0x08

# Width of display = 40. 8 pixels per character width
# Height of display = 11.

class ImageMessage:
	# Expects PIL.Image as img
	def __init__(self, img, speed = 0, mode = Mode.LEFT, flash = False, marquee = False, padImage = False):
		img = img.convert('L')
		self.speed = speed
		self.mode = mode
		self.flash = flash
		self.marquee = marquee

		self.data = ""
		self.len = 0

		if isinstance(img, list):
			for i in range(0, len(img)):
				self.addimg(img[i], padImage)
		else:
			self.addimg(img, padImage)

	def addimg(img, padImage):
		width = img.width
		maxRange = 6 # ceil(44.0 / 8.0)
		if not padImage:
			maxRange = ceil(width / 8.0)
		for i in range(0, maxRange):
			for row in range(0, 11):
				dByte = 0
				for col in range(0, 8):
					xpos = i * 8 + col
					if xpos < width and img.getpixel((xpos, row)) >= 128:
						dByte |= 1 << (7 - col)
				self.data += mkHex(dByte)
			self.len += 1


class RawMessage:
	def __init__(self, data, speed = 0, mode = Mode.LEFT, flash = False, marquee = False):
		self.speed = speed
		self.mode = mode
		self.flash = flash
		self.marquee = marquee

		self.len = ceil(len(data) / 22.0)

class TextMessage:
	def __init__(self, text, speed = 0, mode = Mode.LEFT, flash = False, marquee = False):
		global CHAR_CODES
		self.speed = speed
		self.mode = mode
		self.flash = flash
		self.marquee = marquee

		self.len = 0
		self.data = ""
		for i in range(0, len(text)):
			if not text[i] in CHAR_CODES:
				continue
			self.data = self.data + CHAR_CODES[text[i]]
			self.len += 1

def mkHex(num, pad = 2):
	data = hex(num)[2:]
	if len(data) < pad:
		return ("0" * (pad - len(data))) + data
	return data

def convert(data):
	global PACKET_START
	global PACKET_BYTE_SIZE
	global PACKET_BYTE_SIZE_2
	global MAX_MESSAGES
	global BYTE_ORDER

	if len(data) > MAX_MESSAGES:
		raise ValueError("data must not have more than %d messages" % MAX_MESSAGES)

	emptyMessages = MAX_MESSAGES - len(data)
	

	# set(0, (calendar[Calendar.YEAR] and 0xFF).toByte())
	# set(1, ((calendar[Calendar.MONTH] + 1) and 0xFF).toByte())
	# set(2, (calendar[Calendar.DAY_OF_MONTH] and 0xFF).toByte())
	# set(3, (calendar[Calendar.HOUR_OF_DAY] and 0xFF).toByte())
	# set(4, (calendar[Calendar.MINUTE] and 0xFF).toByte())
	# set(5, (calendar[Calendar.SECOND] and 0xFF).toByte())

	timestampBytes = "E10C06172D23" # TODO

	flashByte = 0
	marqueeByte = 0
	optionBytes = ""
	sizeBytes = ""
	messageBytes = ""

	for i in range(0, len(data)):
		msg = data[i]
		if msg.flash:
			flashByte = flashByte | (1 << i)
		if msg.marquee:
			marqueeByte = marqueeByte | (1 << i)
		optionBytes += mkHex(msg.mode.value | (msg.speed << 4))
		messageBytes += msg.data
		sizeBytes += mkHex(msg.len, 4)

	optionBytes += "00" * emptyMessages
	sizeBytes += "0000" * emptyMessages

	result = PACKET_START + mkHex(flashByte) + mkHex(marqueeByte) + optionBytes + sizeBytes + "000000000000" + timestampBytes + "00000000" + "00000000000000000000000000000000" + messageBytes

	length = len(result)
	padLength = PACKET_BYTE_SIZE_2 - (length % PACKET_BYTE_SIZE_2)
	result += "0" * padLength
	data = unhexlify(result)

	return [data[i:i+PACKET_BYTE_SIZE] for i in range(0, len(data), PACKET_BYTE_SIZE)]
