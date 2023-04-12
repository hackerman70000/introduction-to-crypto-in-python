from random import randrange
from typing import Tuple

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad


def encrypt(key: bytes, data: bytes) -> Tuple[bytes, bytes]:
	# note: this is using CBC mode, which doesn't provide integrity
	# for actual use you should consider a more modern mode like GCM, EAX, CCM, OCB, SIV or whatever is still considered secure at the time you read this
	cipher = AES.new(key, AES.MODE_CBC)
	padded_data = pad(data, AES.block_size)
	# similarly, this should be using encrypt_and_digest, but we're not doing integrity here
	ciphertext = cipher.encrypt(padded_data)
	return ciphertext, cipher.iv


def decrypt(key: bytes, ciphertext: bytes, iv: bytes) -> bytes:
	cipher = AES.new(key, AES.MODE_CBC, iv=iv)
	# again, this should be using decrypt_and_verify, if we cared about integrity
	padded_data = cipher.decrypt(ciphertext)
	try:
		return unpad(padded_data, AES.block_size)
	except ValueError as e:
		print(f"Error while decrypting: {e}")
		print(f"Padded decrypted data (hex): {hex(int.from_bytes(padded_data, 'big'))}")
		raise


def add_error(data: bytes) -> bytes:
	data = bytearray(data)
	for _ in range(randrange(10)):
		data[randrange(len(data))] ^= 1
	return bytes(data)


def keygen() -> bytes:
	return get_random_bytes(16)


def main():
	print("Reading file...")
	with open("Jakub_Bliźniuk_Bartłomiej_Dmitruk.txt", "rb") as f:
		data = f.read()
	print(f"File data: {data.decode()}")
	print(f"Hex data: {hex(int.from_bytes(data, 'big'))}")

	print("Generating key...")
	key = keygen()
	print(f"Key (hex): {hex(int.from_bytes(key, 'big'))}")
	with open("Jakub_Bliźniuk_Bartłomiej_Dmitruk.key", "wb") as f:
		f.write(key)

	print("Encrypting...")
	ciphertext, iv = encrypt(key, data)
	print(f"Ciphertext (hex): {hex(int.from_bytes(ciphertext, 'big'))}")

	with open("Jakub_Bliźniuk_Bartłomiej_Dmitruk.encrypted.txt", "wb") as f:
		f.write(iv)
		f.write(ciphertext)

	print("Decrypting...")
	decrypted = decrypt(key, ciphertext, iv)
	print(f"Decrypted: {decrypted.decode()}")

	try:
		print("Adding errors to ciphertext...")
		ciphertext_error = add_error(ciphertext)
		decrypted = decrypt(key, ciphertext_error, iv)
		print(f"Decrypted with error: {decrypted.decode()}")
	except ValueError:
		pass

	try:
		print("Adding errors to key..")
		key_error = add_error(key)
		decrypted = decrypt(key_error, ciphertext, iv)
		print(f"Decrypted with error: {decrypted.decode()}")
	except ValueError:
		pass


if __name__ == "__main__":
	main()
