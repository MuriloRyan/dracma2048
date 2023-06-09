import bitops

def gethash(entry):
    entry = str(entry)
    hlen, k = 2048, 0
    HASHLEN = hlen // 4

    message = ''.join([str(ord(c)) for c in entry])
    message = bitops.adjust(int(message), length=HASHLEN)
    consthash = ''
    h0 = message

    for _ in range(16):
        kvalue = int(bitops.constK[k], base=16)
        h0 = bitops.shuffle(h0, kvalue, lent=512)
        consthash = consthash + str(kvalue)
        k += 1

    h1 = h0
    for _ in range(16):
        kvalue = int(bitops.constK[k], base=16)
        h1 = bitops.shuffle(h1, kvalue, lent=512)
        consthash = consthash + str(kvalue)
        k += 1
    h2 = ( bitops.adjust( str(h0) + str(h0 | h1), length=1024) )
    
    for _ in range(16):
        kvalue = int(bitops.constK[k], base=16)
        h2 = bitops.shuffle(int(h2), kvalue, lent=1024)
        consthash = consthash + str(kvalue)
        k += 1
    
    h3 = str(h2) + str(h0)
    h3 = bitops.adjust(h3,length=2048)

    for _ in range(16):
        kvalue = int(bitops.constK[k], base=16)
        h3 = bitops.shuffle(int(h3), kvalue, lent=2048)
        consthash = consthash + str(kvalue)
        k += 1

    h4 = h3
    for _ in range(32):
        kvalue = int(bitops.constK[k], base=16)
        h3 = bitops.shuffle(h3, kvalue, lent=2048)
        consthash = consthash + str(kvalue)

    h3list = bitops.getchuncks(h3)
    h4 = bitops.operatechuncks(h3list)

    return hex(h4)[2:]

a = gethash('Omega0')
try:
    print(f"{a}\ncontem:\n{a.bit_length()}")
except:
    print(a)