import collections
import itertools

def gen_primes():
    """ Efficiently generate an infinite sequence of prime numbers.
    """
    # map composite numbers to prime factors
    factors = collections.defaultdict(list)
    for q in itertools.count(2):
        if q not in factors:
            # q is prime: yield q and add next multiple to map
            yield q        
            factors[q * q] = [q]
        else:
            # q is composite: feed-forward prime factors and remove from map
            for p in factors[q]:
                factors[p + q].append(p)
            del factors[q]


# testing
if __name__ == "__main__":
    gen = gen_primes()
    for _ in range(20):
        print(next(gen))