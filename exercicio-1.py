def cifrar(texto: str, k: int) -> str:

    resultado = []
    for c in texto:
        if c.isalpha():
            base = 'A' if c.isupper() else 'a'
            novo_char = chr((ord(c) - ord(base) + k) % 26 + ord(base))
            resultado.append(novo_char)
        else:
            resultado.append(c)
    return ''.join(resultado)

def decifrar(texto: str, k: int) -> str:

    return cifrar(texto, -k)  

def ataque_forca_bruta(texto_cifrado: str):

    print("\nAtaque por força bruta:")
    for k in range(26):
        print(f"Chave {k:2d}: {decifrar(texto_cifrado, k)}")

FREQUENCIAS_PORTUGUES = {
    'a': 14.63, 'b': 1.04, 'c': 3.88, 'd': 4.99, 'e': 12.57,
    'f': 1.02, 'g': 1.30, 'h': 1.28, 'i': 6.18, 'j': 0.40,
    'k': 0.02, 'l': 2.78, 'm': 4.74, 'n': 5.05, 'o': 10.73,
    'p': 2.52, 'q': 1.20, 'r': 6.53, 's': 7.81, 't': 4.34,
    'u': 4.63, 'v': 1.67, 'w': 0.01, 'x': 0.21, 'y': 0.01,
    'z': 0.47
}

def ataque_frequencia(texto_cifrado: str) -> int:

    from collections import defaultdict

    contagem = defaultdict(int)
    total_letras = 0
    
    for c in texto_cifrado.lower():
        if c.isalpha():
            contagem[c] += 1
            total_letras += 1
    
    if total_letras == 0:
        return 0  # Não há letras para analisar
    
    frequencias_obs = {letra: (cont / total_letras) * 100 
                      for letra, cont in contagem.items()}
    
    melhor_teste = -1
    melhor_chave = 0
    
    for k in range(26):
        teste = 0
        for letra_cifrada, freq_obs in frequencias_obs.items():
            letra_original = chr((ord(letra_cifrada) - ord('a') - k) % 26 + ord('a'))
            teste += freq_obs * FREQUENCIAS_PORTUGUES.get(letra_original, 0)
        
        if teste > melhor_teste:
            melhor_teste = teste
            melhor_chave = k
    
    print(f"\nAtaque por frequência - Melhor chave encontrada: {melhor_chave}")
    print(f"Texto decifrado: {decifrar(texto_cifrado, melhor_chave)}")
    
    return melhor_chave

def main():
    # teste
    texto_original = input('escreva o texto:')
    chave = 3
    
    # Cifrar
    texto_cifrado = cifrar(texto_original, chave)
    print(f"Texto original: {texto_original}")
    print(f"Texto cifrado: {texto_cifrado}")
    
    # Decifrar
    texto_decifrado = decifrar(texto_cifrado, chave)
    print(f"Texto decifrado: {texto_decifrado}")
    
    # Ataques
    ataque_forca_bruta(texto_cifrado)
    ataque_frequencia(texto_cifrado)

if __name__ == "__main__":
    main()
