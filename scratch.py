MOD = 10**6 + 3

binpow = []
def precompute():
    n = 1
    for _ in range(30):
        binpow.append(n)
        n *= 2
        n = n % MOD

    
precompute()
print(binpow)