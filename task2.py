from random import choice, getrandbits, random, randrange
from secrets import choice as secrets_choice
from secrets import randbelow, randbits

from randcrack import RandCrack
from Crypto.Util.number import getPrime, getStrongPrime

def break_random(randbit_list: list[int]) -> RandCrack:
	rc = RandCrack()
	for i in randbit_list:
		rc.submit(i)
	return rc


def main():
	print("Python includes two libraries for generating random numbers - random and secrets")
	print(
	    "random is a basic pseudo-random number generator (MT19937), and secrets is a cryptographically secure random number generator"
	)
	print(
	    "they only really share two functions - getrandbits (called randbits in secrets) and choice"
	)
	print("getrandbits returns a random integer with k random bits")
	print(
	    f"for example, getrandbits(10) returns a random integer between 0 and 1023. For instance it might be: {getrandbits(10)}"
	)
	print(
	    f"randbits is the same, but it's using system randomness instead of a pseudo-random number generator. A call to randbits(10) might return: {randbits(10)}"
	)
	print(
	    f"choice returns a random element from a sequence. For example, choice('abcdefg') returns one random letter of these three. For instance it might be: {choice('abcdefg')}"
	)
	print(
	    f"again, secrets.choice is the same with a better (but slower) randomness. A call to secrets.choice('abcdefg']) might return: {secrets_choice('abcdefg')}"
	)
	# TODO: do randrange and randbelow, mention token generation (secrets) and some other functions random has

	print("\nNow let's try to break the random number generator")
	print("We'll use the first 624 random numbers to predict the next one")
	random_results = [getrandbits(32) for _ in range(624)]
	print(
	    f"Some of our 624 random numbers: [{str(random_results[:5])[1:-1]}, ..., {str(random_results[-5:])[1:-1]}]"
	)
	break_random(random_results)
	print("\nNow let's try to predict the next random number")
	rc = break_random(random_results)

	print(f"{'Predicted:':<17} {rc.predict_getrandbits(32)}")
	actual = getrandbits(32)
	print(f"{'Actual:':<17} {actual}")
	print(
	    "\nThis finds the internal state of the random number generator, so it will predict the results from most functions from the random library"
	)
	print("For example, we can predict the random() function")
	print(f"{'Predicted:':<17} {rc.predict_random()}")
	print(f"{'Actual:':<17} {random()}")

	print("\nThis doesn't work for secrets, because it uses system randomness")
	print(
	    "For example, submitting the first 624 random numbers from randbits doesn't work, these two number will almost certainly be different:"
	)
	s_random_results = [randbits(32) for _ in range(624)]
	s_rc = break_random(s_random_results)
	print(f"{'Predicted:':<17} {s_rc.predict_getrandbits(32)}")
	print(f"{'Actual (secrets):':<17} {randbits(32)}")

	# pycryptodome

	print("\n\nUse of PyCryptodome package")

	print("\nThere is two functions in this package that generate random prime numbers:")
	print("- getPrime() returns a random N-bit prime number")             
	print("             parameters : N, randfunc(optional)")
	random_prime = getPrime(128)
	print(f"{'  Random prime (128 bits): ':<35} {random_prime}")
 #the exact length of the strong prime. It must be a multiple of 128 and > 512
	print("\n- getStrongPrime() returns a random strong N-bit prime number. In this context, p is a strong prime if p-1 and p+1 have at least one large prime factor, parameters : N, randfunc(optional)")
	print("             parameters : N - It must be a multiple of 128 and > 512, e -if provided, the returned prime (minus 1) will be coprime to e and thus suitable for RSA where e is the public exponent")
	print("                          false_positive_prob (float) – The statistical probability for the result not to be actually a prime. It defaults to 10^-6")
	print("                          randfunc(optional)")
	strong_random_prime = getStrongPrime(512)
	print(f"{'  Strong random prime (512 bits): ':<35} {strong_random_prime}") 


if __name__ == "__main__":
	main()
