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

import random
import string

def generate_similar_strings(base_string, num_strings, num_differences):
    similar_strings = []

    for _ in range(num_strings):
        # Criar uma lista de caracteres para a nova string
        new_string = list(base_string)

        # Gerar posições aleatórias para as diferenças
        positions = random.sample(range(len(base_string)), num_differences)

        # Alterar os caracteres nessas posições
        for pos in positions:
            new_char = random.choice(string.ascii_letters)
            while new_char == base_string[pos]:
                new_char = random.choice(string.ascii_letters)
            new_string[pos] = new_char

        # Adicionar a nova string à lista
        similar_strings.append("".join(new_string))

    return similar_strings

# Valor base único
base_value = "Eu não sei o que fazer agora, mas vamos testar."

# Gerar 10 strings semelhantes com 5 diferenças em cada uma
similar_strings = generate_similar_strings(base_value, 10, 5)

# Imprimir as strings geradas com seus valores e número de bits iguais
for string in similar_strings:
    num_bits_iguais = sum(a == b for a, b in zip(gethash(base_value), string)) * 8
    print(f"String: {string}")
    print(f"Valor: {gethash(string)}")
    print(f"Número de bits iguais: {num_bits_iguais}")
    print("-" * 30)
