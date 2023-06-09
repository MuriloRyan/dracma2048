constK = [
    "428a2f98d728ae22", "7137449123ef65cd", "b5c0fbcfec4d3b2f", "e9b5dba58189dbbc",
    "3956c25bf348b538", "59f111f1b605d019", "923f82a4af194f9b", "ab1c5ed5da6d8118",
    "d807aa98a3030242", "12835b0145706fbe", "243185be4ee4b28c", "550c7dc3d5ffb4e2",
    "72be5d74f27b896f", "80deb1fe3b1696b1", "9bdc06a725c71235", "c19bf174cf692694",
    "e49b69c19ef14ad2", "efbe4786384f25e3", "0fc19dc68b8cd5b5", "240ca1cc77ac9c65",
    "2de92c6f592b0275", "4a7484aa6ea6e483", "5cb0a9dcbd41fbd4", "76f988da831153b5",
    "983e5152ee66dfab", "a831c66d2db43210", "b00327c898fb213f", "bf597fc7beef0ee4",
    "c6e00bf33da88fc2", "d5a79147930aa725", "06ca6351e003826f", "142929670a0e6e70",
    "27b70a8546d22ffc", "2e1b21385c26c926", "4d2c6dfc5ac42aed", "53380d139d95b3df",
    "650a73548baf63de", "766a0abb3c77b2a8", "81c2c92e47edaee6", "92722c851482353b",
    "a2bfe8a14cf10364", "a81a664bbc423001", "c24b8b70d0f89791", "c76c51a30654be30",
    "d192e8196ef5218", "d69906245565a910", "f40e35855771202a", "106aa07032bbd1b8",
    "19a4c116b8d2d0c8", "1e376c085141ab53", "2748774cdf8eeb99", "34b0bcb5e19b48a8",
    "391c0cb3c5c95a63", "4ed8aa4ae3418acb", "5b9cca4f7763e373", "682e6ff3d6b2b8a3",
    "748f82ee5defb2fc", "78a5636f43172f60", "84c87814a1f0ab72", "8cc702081a6439ec",
    "90befffa23631e28", "a4506cebde82bde9", "bef9a3f7b2c67915", "c67178f2e372532b",
    "ca273eceea26619c", "d186b8c721c0c207", "eada7dd6cde0eb1e", "f57d4f7fee6ed178",
    "06f067aa72176fba", "0a637dc5a2c898a6", "113f9804bef90dae", "1b710b35131c471b",
    "28db77f523047d84", "32caab7b40c72493", "3c9ebe0a15c9bebc", "431d67c49c100d4c",
    "4cc5d4becb3e42b6", "597f299cfc657e2a", "5fcb6fab3ad6faec", "6c44198c4a475817"
]

def adjust(message, length=2048):
    message = int(message)

    if message.bit_length() < length:
        message = int(bin(message)[2:]+'1',base=2)
        message = message << (length - message.bit_length())
    elif message.bit_length() > length:
        message = message >> (message.bit_length() - length)

    return message

def shuffle(binary_sequence, k, lent=None):
    if not lent:
        lent = binary_sequence.bit_length()

    binary_list = list(bin(adjust(binary_sequence, length=lent))[2:])
    n = len(binary_list)

    for i in range(n - 1, 0, -1):
        j = k % (i + 1)
        binary_list[i], binary_list[j] = binary_list[j], binary_list[i]

    shuffled_sequence = ''.join(binary_list)
    return int(shuffled_sequence, 2)


def getchuncks(binary):
    binary = bin(binary)[2:] if isinstance(binary,int) else str(binary)
    chuncks = []

    for i in range(0, 2048, 256):
        block = binary[i:i+256]
        chuncks.append(block)

    chuncks = [int(n) for n in chuncks]

    return chuncks

def operatechuncks(chuncks):
    
    BigsideA = chuncks[0:4]
    BigsideB = chuncks[4:8]

    sda = int(''.join(str(i) for i in BigsideB[len(BigsideB)//2:]))
    sdb = int(''.join(str(i) for i in BigsideB[len(BigsideB)//2:]))
    sdx = bin(int(''.join([str(sda^sdb),str(sdb)])))[2:]

    BigsideA = int(''.join(str(i) for i in BigsideA))^int(''.join(str(i) for i in BigsideB))

    hashToOp = ''.join([str(BigsideA),sdx])
    hashToOp = getchuncks(hashToOp)

    p0 = (hashToOp[4] ^ hashToOp[5]) ^ hashToOp[7]
    p1 = (p0 ^ (hashToOp[0]^hashToOp[1]) ) ^ hashToOp[6]

    returnhash = [  p0^p1,hashToOp[1],hashToOp[2],hashToOp[3],
            hashToOp[4],hashToOp[5],hashToOp[6],hashToOp[7]]
    
    returnhash = adjust(''.join([str(i) for i in returnhash]),length=2048)

    return returnhash