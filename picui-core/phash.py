import Image
import ImageFilter
from bitarray import bitarray

class ImageHash(object):
	def __init__(self, path, size=8):
		self.image_path = path
		self.hash_size = size
		self.image = Image.open(path)

	def average_hash(self):
		image = self.image.resize((self.hash_size, self.hash_size), Image.NEAREST).convert("L")
		pixels = list(image.getdata())
		avg = sum(pixels) / len(pixels)
		diff = []
		for pixel in pixels:
			value = 1 if pixel > avg else 0
			diff.append(str(value))

		ba = bitarray("".join(diff), endian="little")
		return ba.tobytes().encode('hex')

	def dct_hash(self):
		image = self.image.resize((32,32), Image.NEAREST).convert("L")
		#pixels = list(image.getdata())
		pixels = image.load()
		width, height = image.size

		reduced = []

		for i in range(0,8):
			for j in range(0,8):
				reduced.append(pixels[i,j])


		avg = (sum(reduced) - reduced[0]) / (len(reduced) - 1)
		diff = []

		for pixel in reduced:
			value = 1 if pixel > avg else 0
			diff.append(str(value))

		ba = bitarray("".join(diff), endian="little")
		return ba.tobytes().encode('hex')

	def edge_hash(self):
		image = self.image.filter(ImageFilter.CONTOUR).resize((32,32), Image.NEAREST).convert("L")
		#pixels = list(image.getdata())
		pixels = image.load()
		width, height = image.size

		reduced = []

		for i in range(0,8):
			for j in range(0,8):
				reduced.append(pixels[i,j])


		avg = (sum(reduced) - reduced[0]) / (len(reduced) - 1)
		diff = []

		for pixel in reduced:
			value = 1 if pixel > avg else 0
			diff.append(str(value))

		ba = bitarray("".join(diff), endian="little")
		return ba.tobytes().encode('hex')

	def blur_hash(self):

		image = self.image.filter(ImageFilter.BLUR).filter(ImageFilter.CONTOUR).resize((32,32), Image.NEAREST).convert("L")
		#pixels = list(image.getdata())
		pixels = image.load()
		width, height = image.size

		reduced = []

		for i in range(0,8):
			for j in range(0,8):
				reduced.append(pixels[i,j])


		avg = (sum(reduced) - reduced[0]) / (len(reduced) - 1)
		diff = []

		for pixel in reduced:
			value = 1 if pixel > avg else 0
			diff.append(str(value))

		ba = bitarray("".join(diff), endian="little")
		return ba.tobytes().encode('hex')


def hamming_distance(image1, image2): #image1 and image2 are two bitarrays encoded in hex
	dist = 0
	for i in range(0, len(image1)):
		if (image1[i] == image2[i]):
			pass
		else:
			dist += 1
	return dist

if __name__ == "__main__":
	print "STARTING"
	hash1 = ImageHash('sample_images/PinkiePieHiRes.png').blur_hash()
	hash2 = ImageHash('sample_images/obama3.jpg').edge_hash()
	print hash1
	print hash2
	print hamming_distance(hash1,hash2)