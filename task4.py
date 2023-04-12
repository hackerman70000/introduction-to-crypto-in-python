from Cryptodome.Hash import MD5, SHA3_256, SHA256

filename = "Jakub_Bliźniuk_Bartłomiej_Dmitruk.txt"

hash_SHA_256 = SHA256.new()
hash_MD5 = MD5.new()
hash_SHA3_256 = SHA3_256.new()

with open(filename, "w") as f:
	f.write("To wiadomość do zaszyfrowania")

with open(filename, "rb") as f:
	while data := f.read(1024):
		hash_SHA_256.update(data)
		hash_MD5.update(data)
		hash_SHA3_256.update(data)

print("\nHashed text in original file: \n  SHA-256: ", hash_SHA_256.hexdigest())
print("  SHA3-256: ", hash_SHA3_256.hexdigest())
print("  MD5: ", hash_MD5.hexdigest())

with open(filename, "w") as f:
	f.write("Ta wiadomość do zaszyfrowania")

hash2_SHA_256 = SHA256.new()
hash2_MD5 = MD5.new()
hash2_SHA3_256 = SHA3_256.new()

with open(filename, "rb") as f:
	while data := f.read(1024):
		hash2_SHA_256.update(data)
		hash2_MD5.update(data)
		hash2_SHA3_256.update(data)

print("\nHashed text in modified file: \n  SHA-256: ", hash2_SHA_256.hexdigest())
print("  SHA3-256: ", hash2_SHA3_256.hexdigest())
print("  MD5: ", hash2_MD5.hexdigest())

print("\n Hash values of original and modified file in:")
if hash_SHA_256.hexdigest() == hash2_SHA_256.hexdigest():
	print(" SHA-256 are the same.")
else:
	print(" SHA-256 differ.")

if hash_SHA3_256.hexdigest() == hash2_SHA3_256.hexdigest():
	print(" SHA3-256 are the same.")
else:
	print(" SHA3-256 differ.")

if hash_MD5.hexdigest() == hash2_MD5.hexdigest():
	print(" MD5 are the same.")
else:
	print(" MD5 differ.")

with open(filename, "w") as f:
	f.write("To wiadomość do zaszyfrowania")
