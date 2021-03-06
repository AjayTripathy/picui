import Image
import ImageFilter
from bitarray import bitarray
import scipy
from scipy import ndimage
from scipy import misc

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

		'''
		tempPixels = misc.fromimage(self.image)
		tempArray = ndimage.gaussian_filter(tempPixels, sigma=3)
		temp = misc.toimage(tempArray)
		temp.save("BLUR.jpg","JPEG")
		'''

		#temp = misc.toimage(ndimage.gaussian_filter(misc.fromimage(self.image),sigma=3))
		#temp.save("BLUR.jpg","JPEG")

		image = color_blur(self.image).filter(ImageFilter.CONTOUR).resize((32,32), Image.NEAREST).convert("L")
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


def color_blur(image):
	im = scipy.array(image)
	im2 = scipy.zeros(im.shape)

	for i in range(3):
		im2[:,:,i] = ndimage.filters.gaussian_filter(im[:,:,i],5)

	#im2 = scipy.uint8(im2)
	toReturn = misc.toimage(im2)
	toReturn.save("BLUR.jpg","JPEG")
	return toReturn

if __name__ == "__main__":
	print "STARTING"
	hash1 = ImageHash('sample_images/obama1.jpg').blur_hash()
	hash2 = ImageHash('sample_images/obama2.jpg').blur_hash()
	print hash1
	print hash2
	print hamming_distance(hash1,hash2)