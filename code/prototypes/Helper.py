import numpy as np

def lowest_primes(n):
    return primes(n**2)[:n]


def primes(upto):
    primes = np.arange(3, upto+1, 2)

    isprime = np.ones(int((upto-1)/2), dtype=bool)

    for factor in primes[:int(np.sqrt(upto))]:

        if isprime[int((factor-2)/2)]:
            isprime[int((factor*3-2)/2)::factor] = 0

    return np.insert(primes[isprime], 0, 2)

def hash(states):
    n = states.shape[1] if len(states.shape) > 1 else len(states)
    ps = np.sqrt(lowest_primes(n))
    
    return states.dot(ps)

