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

    h4 = str(h3)[:HASHLEN*2]
    h5 = str(h3)[HASHLEN*2:]

    h6 = str(h4)+str(h5)
    for _ in range(32):
        h6 = bitops.shuffle(h6, kvalue, lent=2048)
        consthash = consthash + str(kvalue)

    blocks = []
    h6 = bin(h6)[2:]
    for i in range(0, 2048, 256):
        block = h6[i:i+256]
        blocks.append(block)
    
    #1024 bits
    h6Lda = ''.join(blocks[0:4])
    h6Ldb = ''.join(blocks[4:8])

    #512 bits
    ldA = int(''.join(h6Ldb[:len(h6Ldb)//2]), base=2)
    ldB = int(''.join(h6Ldb[len(h6Ldb)//2:]),base=2)
    ldX = bin(int(''.join([str(ldB^ldA),str(ldB)])))[2:]

    h7 = ''.join([str(h6Lda),str(ldX)])
    h7 = int(h7,base=2)
    h7 = int (bitops.adjust(h7,length=2048) )
    h7 = bitops.adjust(h7,length=2048)

    h7list = []
    h7 = bin(h7)[2:]
    for i in range(0, 2048, 256):
        block = h6[i:i+256]
        h7list.append(block)
    h7list = [int(n,base=2) for n in h7list]

    p0 = (h7list[4] ^ h7list[5]) ^ h7list[7]
    p1 = (p0 ^ (h7list[0]^h7list[1]) ) ^ h7list[6]

    h8 = [  p0^p1,h7list[1],h7list[2],h7list[3],
            h7list[4],h7list[5],h7list[6],h7list[7]]
    
    h8 = bitops.adjust(''.join([str(i) for i in h8]),length=2048)

    return int(h8)