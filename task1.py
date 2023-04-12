from itertools import chain
from random import choices
from typing import Self

from Cryptodome.Util.number import getPrime, isPrime


class ModularInt():

	def __init__(self, value: int, mod: int) -> None:
		self.value: int = value % mod
		self.mod: int = mod

	def __add__(self, other: int) -> Self:
		return ModularInt(self.value + other.value, self.mod)

	def __sub__(self, other: int):
		return ModularInt(self.value - other.value, self.mod)

	def __mul__(self, other):
		return ModularInt(self.value * other.value, self.mod)

	def __truediv__(self, other):
		return ModularInt(self.value / other.value, self.mod)

	def __floordiv__(self, other):
		return ModularInt(self.value // other.value, self.mod)

	def inverse(self):
		return ModularInt(pow(self.value, -1, self.mod), self.mod)

	def __int__(self):
		return self.value


def mod_add(a, b, mod):
	return int(ModularInt(a, mod) + ModularInt(b, mod))


def mod_sub(a, b, mod):
	return int(ModularInt(a, mod) - ModularInt(b, mod))


def mod_mul(a, b, mod):
	return int(ModularInt(a, mod) * ModularInt(b, mod))


def mod_inv(a, mod):
	return int(ModularInt(a, mod).inverse())


def prime_range(start, stop):
	for i in range(start, stop):
		if isPrime(i):
			yield i


def main():
	for i in chain(choices(prime_range(10, 100), k=4), [getPrime(1024)]):
		for j in choices(range(10, min(i, 1024)), k=2):
			for k in choices(range(10, min(i, 1024)), k=2):
				print(f"{k} + {j} = {mod_add(k, j, i)} (mod {i})")
				print(f"{k} - {j} = {mod_sub(k, j, i)} (mod {i})")
				print(f"{k} * {j} = {mod_mul(k, j, i)} (mod {i})")
			try:
				print(f"{j}^-1 = {mod_inv(j, i)} (mod {i})")
			except:
				print(f"{j}^-1 mod {i} doesn't exist - this is not a prime finite field!")


if __name__ == "__main__":
	main()
