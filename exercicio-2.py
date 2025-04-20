def cifrar_transposicao(texto: str, chave: int) -> str:

    texto = texto.lower().replace(" ", "")
    
    num_colunas = chave
    num_linhas = (len(texto) + num_colunas - 1) // num_colunas 
    
    # Preenche com 'x' para completar a matriz (se precisar)
    texto += 'x' * (num_linhas * num_colunas - len(texto))
    
    matriz = []
    for i in range(num_linhas):
        inicio = i * num_colunas
        fim = inicio + num_colunas
        matriz.append(list(texto[inicio:fim]))
    
    texto_cifrado = []
    for col in range(num_colunas):
        for linha in range(num_linhas):
            texto_cifrado.append(matriz[linha][col])
    
    return ''.join(texto_cifrado)

def decifrar_transposicao(texto_cifrado: str, chave: int) -> str:

    num_colunas = chave
    num_linhas = (len(texto_cifrado) + num_colunas - 1) // num_colunas
    
    matriz = [['' for _ in range(num_colunas)] for _ in range(num_linhas)]
    
    pos = 0
    for col in range(num_colunas):
        for linha in range(num_linhas):
            if pos < len(texto_cifrado):
                matriz[linha][col] = texto_cifrado[pos]
                pos += 1
    
    texto_decifrado = []
    for linha in range(num_linhas):
        for col in range(num_colunas):
            texto_decifrado.append(matriz[linha][col])
    
    return ''.join(texto_decifrado).rstrip('x')

def ataque_forca_bruta(texto_cifrado: str, max_chave: int = 20) -> dict:

    resultados = {}
    tamanho = len(texto_cifrado)
    
    for chave in range(1, min(max_chave, tamanho) + 1):
        try:
            decifrado = decifrar_transposicao(texto_cifrado, chave)
            resultados[chave] = decifrado
        except Exception as e:
            print(f"Erro com chave {chave}: {e}")
            continue
    
    return resultados

FREQUENCIAS_PT = {
    'a': 14.63, 'b': 1.04, 'c': 3.88, 'd': 4.99, 'e': 12.57,
    'f': 1.02, 'g': 1.30, 'h': 1.28, 'i': 6.18, 'j': 0.40,
    'k': 0.02, 'l': 2.78, 'm': 4.74, 'n': 5.05, 'o': 10.73,
    'p': 2.52, 'q': 1.20, 'r': 6.53, 's': 7.81, 't': 4.34,
    'u': 4.63, 'v': 1.67, 'w': 0.01, 'x': 0.21, 'y': 0.01,
    'z': 0.47
}

def calcular_cont(texto: str) -> float:
    #Calcula o contador baseado na frequência de letras em Português
    contagem = {}
    total = 0
    
    for c in texto.lower():
        if c in FREQUENCIAS_PT:
            contagem[c] = contagem.get(c, 0) + 1
            total += 1
    
    if total == 0:
        return 0.0
    
    # Calcula o contador de similaridade com o Português
    cont = 0.0
    for letra, freq_pt in FREQUENCIAS_PT.items():
        freq_obs = (contagem.get(letra, 0) / total) * 100
        cont += min(freq_obs, freq_pt) 
    
    return cont

def ataque_frequencia(texto_cifrado: str, max_chave: int = 20) -> list:

    candidatos = []
    tamanho = len(texto_cifrado)
    
    for chave in range(1, min(max_chave, tamanho) + 1):
        try:
            decifrado = decifrar_transposicao(texto_cifrado, chave)
            cont = calcular_cont(decifrado)
            candidatos.append({'chave': chave, 'cont': cont, 'texto': decifrado})
        except Exception as e:
            print(f"Erro com chave {chave}: {e}")
            continue
    
    candidatos_ordenados = sorted(candidatos, key=lambda x: x['cont'], reverse=True)
    
    return candidatos_ordenados[:5]

# exemplo
texto_original = "criptografar um texto grande só pra testar a transposição e os ataques de força bruta e frequência :)"
chave = 4

# Cifração
texto_cifrado = cifrar_transposicao(texto_original, chave)
print(f"Texto original: {texto_original}")
print(f"Texto cifrado: {texto_cifrado}")

# Decifração
texto_decifrado = decifrar_transposicao(texto_cifrado, chave)
print(f"Texto decifrado: {texto_decifrado}")

# Ataque por força bruta
print("\nResultados do ataque por força bruta:")
resultados_bruta = ataque_forca_bruta(texto_cifrado)
for chave, texto in resultados_bruta.items():
    print(f"Chave {chave}: {texto}")

# Ataque por frequência
print("\nResultados do ataque por frequência:")
resultados_freq = ataque_frequencia(texto_cifrado)
for resultado in resultados_freq:
    print(f"Chave {resultado['chave']} (Score: {resultado['cont']:.2f}): {resultado['texto']}")
