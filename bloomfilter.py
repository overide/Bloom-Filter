# Python 3 program to build Bloom Filter

import math
import mmh3
from bitarray import bitarray

class BloomFilter(object):
	'''
	Class for Bloom filter

	A Bloom filter is a space-efficient probabilistic data structure
	It is used to test whether an element is a member of a set.
	details : https://en.wikipedia.org/wiki/Bloom_filter

	class variables
	---------------
	fp_prob : float
		False posible probability in decimal
	size : int
		Size of bit array to use
	hash_count : int
		number of hash functions to use
	bit_array : bitarray
		Bit array of given size

	Hashing Function
	----------------
	Non cryptographic MurMurHash3 is used in this implementation
	more details : https://en.wikipedia.org/wiki/MurmurHash
	'''

	def __init__(self, items_count,fp_prob):
		'''
		Initialize the class variables 

		Parameters
		---------
		items_count : int
			Number of items expected to be stored in bloom filter
		fp_prob : float
			False Positive probability in decimal

		'''
		self.fp_prob = fp_prob
		self.size = self.get_size(items_count,fp_prob)
		self.hash_count = self.get_hash_count(self.size,items_count)
		self.bit_array = bitarray(self.size)
		self.bit_array.setall(0)

	def add(self, item):
		'''
		Add an item in the filter

		Parameters
		----------
		item : bytes like object (string)
			Any item like "geeks" etc.
		'''
		digests = []
		for i in range(self.hash_count):

			# create digest for given item.
			# i work as seed to mmh3.hash() function 
			# With different seed, digest created is different
			digest = mmh3.hash(item,i) % self.size
			digests.append(digest)

			#set the bit True in bit_array
			self.bit_array[digest] = True

	def check(self, item):
		'''
		Check for existence of an item in filter

		Parameters
		----------
		item : bytes like object (string)
			Any item like "geeks" etc.
		'''
		for i in range(self.hash_count):
			digest = mmh3.hash(item,i) % self.size
			if self.bit_array[digest] == False:
				# if any of bit is False then,its not present in filter
				# else there is probability that it exist
				return False
		return True

	@classmethod
	def get_size(self,n,p):
		'''
		Return the size of bit array(m) to used using following formula
		m = -(n * lg(p)) / (lg(2)^2)
		Parameters
		----------
		n : int
			number of items expected to be stored in filter
		p : float
			False Positive probability in decimal
		'''
		m = -(n * math.log(p))/(math.log(2)**2)
		return int(m) 

	@classmethod
	def get_hash_count(self,m,n):
		'''
		Return the hash function(k) to be used using following formula
		k = (m/n) * lg(2)
		Parameters
		----------
		m : int
			size of bit array
		n : int
			number of items expected to be stored in filter
		'''
		k = (m/n) * math.log(2)
		return int(k)