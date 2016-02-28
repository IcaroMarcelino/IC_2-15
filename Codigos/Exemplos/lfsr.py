# Icaro Marcelino Miranda
# Algoritimo LFSR
#
# Gerando numeros pseudo aleatorios de n bits, com uma semente e os expoentes do
# polinomio caracteristico.
#

def lfsr(semente, expoentes, nBits):
    estadoInicial = semente
    lfsr = estadoInicial
    periodo = 0

    for exp in expoentes:
        exp = nBits - exp

    # Usando logica propsicional, defini xor como (p V q) ^ ~(p ^ q).

    while True:
        marca = 0

        for exp in expoentes:
            if (marca == 0):
                bit  = (lfsr >> exp)
                marca = 1

            else:
                # Aqui faco (p V q) para os bits que representam
                # os termos do polinomio caracteristico

                bit ^= (lfsr >> exp)    

        # Aqui temos ~(p ^ q)
        bit &= 1

        # Fazendo o shift de bits.
        lfsr = (lfsr >> 1) | (bit << (nBits - 1))
        periodo += 1

        print(lfsr)

        if (lfsr == estadoInicial):
            print("\nSemente: ", lfsr)
            print("Total de numeros gerados: ", periodo)

            if (periodo == 2**nBits - 1):
                print("Polinomio Maximal\n")

            break