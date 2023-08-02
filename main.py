import random
from timeit import default_timer as timer


def trial_primality_test(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0:
            return False
    return True


def wilson_theorem(n):
    fac = 1
    for i in range(1, n):   # from 1 to n-1
        fac = (fac * i) % n
    return (fac == n-1)


def fermat_primality_test(n, k):
    if n <= 1:
        return False
    if n == 2:
        return True
    for i in range(k):
        a = random.randrange(2, n)  # 2 <= a <= n-1
        if pow(a, n-1, n) != 1:     # compute a^(n-1) mod n
            return False            # definitely composite
    else:
        return True


def miller_rabin_primality_test(n, k):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False    # speedup

    # now n is odd > 3
    s = 0
    d = n-1
    while d % 2 == 0:
        s += 1
        d //= 2
    # n = 2^s * d where d is odd

    for i in range(k):
        a = random.randrange(2, n-1)    # 2 <= a <= n-2
        x = (a**d) % n
        if x == 1:
            continue
        for j in range(s):
            if x == n-1:
                break
            x = (x * x) % n
        else:
            return False
    return True


def expand_x_1(n):
    c = 1
    for i in range(n//2+1):
        c = c*(n-i)//(i+1)
        yield c


def aks_primality_test(p):
    if p == 1:
        return False
    if p == 2:
        return True

    for i in expand_x_1(p):
        if i % p:
            return False
    return True


primes = []

start = 1_000_000_000
end = 1_001_000_000

total_time_trial = 0

total_time_wilson = 0
willson_correct = 0

total_time_fermat = 0
fermat_correct = 0

total_time_miller_rabin = 0
miller_rabin_correct = 0

total_time_aks = 0
aks_correct = 0

start_timer = 0
end_timer = 0

iteration = 5

print("Benchmarking...")

for i in range(start, end+1):

    # trail test
    start_timer = timer()
    result = trial_primality_test(i)
    end_timer = timer()

    total_time_trial += end_timer-start_timer
    primes.append(result)

    # wilson test
    start_timer = timer()
    result = wilson_theorem(i)
    end_timer = timer()

    if (result == primes[i-start]):
        willson_correct += 1
    total_time_wilson += end_timer-start_timer

    # fermat test
    start_timer = timer()
    result = fermat_primality_test(i, iteration)
    end_timer = timer()

    if (result == primes[i-start]):
        fermat_correct += 1
    total_time_fermat += end_timer-start_timer

    # miller_rabin test
    start_timer = timer()
    result = miller_rabin_primality_test(i, iteration)
    end_timer = timer()

    if (result == primes[i-start]):
        miller_rabin_correct += 1
    total_time_miller_rabin += end_timer-start_timer

    # aks test
    start_timer = timer()
    result = aks_primality_test(i)
    end_timer = timer()
    if (result == primes[i-start]):
        aks_correct += 1
    total_time_aks += end_timer-start_timer

print(fermat_correct)
print("Finished bencemark")

print("Trail Primality Test. Accuracy: {:.3f}\tTime total: {:3f}".format(
    100, total_time_trial))
print("Wilson Primality Test. Accuracy: {:.3f}\tTime total: {:3f}".format(willson_correct*100 /
      (end-start+1), total_time_wilson))
print("Fermat Primality Test. Accuracy: {:.3f}\tTime total: {:3f}".format(fermat_correct*100 /
      (end-start+1), total_time_fermat))
print("Miller-Rabin Primality Test. Accuracy: {:.3f}\tTime total: {:3f}".format(miller_rabin_correct*100 /
      (end-start+1), total_time_miller_rabin))
print("AKS Primality Test. Accuracy: {:.3f}\tTime total: {:3f}".format(aks_correct*100 /
      (end-start+1), total_time_aks))
