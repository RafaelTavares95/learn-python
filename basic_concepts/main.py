from enum import Enum

print("Hello")

# variaveis
# Variáveis (snake_case)
nome = "Python"
idade = 30
altura = 1.75
ativo = True

# Tipos básicos
texto = str("Hello")       # String
numero = int(42)           # Inteiro
decimal = float(3.14)      # Float
booleano = bool(True)      # Boolean

# Lista (mutável)
frutas = ["maçã", "banana", "laranja"]

# Tupla (imutável)
coordenadas = (10, 20)

# Dicionário
pessoa = {
    "nome": "João",
    "idade": 25,
    "cidade": "São Paulo"
}

# Conjunto
numeros_unicos = {1, 2, 3, 4, 5}

# Aritméticos
soma = 5 + 3        # 8
subtracao = 10 - 4  # 6
multiplicacao = 3 * 4  # 12
divisao = 15 / 3    # 5.0
divisao_inteira = 15 // 4  # 3
resto = 15 % 4      # 3
potencia = 2 ** 3   # 8

# Comparação
igual = 5 == 5      # True
diferente = 5 != 3  # True
maior = 10 > 5      # True
menor_igual = 3 <= 5  # True

# Lógicos
e_logico = True and False    # False
ou_logico = True or False    # True
negacao = not True          # False

# Condicional
idade = 18
if idade >= 18:
    print("Maior de idade")
elif idade >= 16:
    print("Pode votar")
else:
    print("Menor de idade")

# Loop for
for i in range(5):
    print(f"Número: {i}")

for fruta in ["maçã", "banana"]:
    print(fruta)

# Loop while
contador = 0
while contador < 5:
    print(contador)
    contador += 1

# Função simples
def saudacao(nome):
    return f"Olá, {nome}!"

# Função com parâmetro padrão
def calcular_area(largura, altura=1):
    return largura * altura

# Função com múltiplos retornos
def operacoes(a, b):
    return a + b, a - b, a * b

# Chamadas
resultado = saudacao("Python")
area = calcular_area(5, 3)
soma, sub, mult = operacoes(10, 5)    






# Test
name = "Rafa"
a_height = 1.98
a_weight = 120



class Status(Enum):
    MAGREZA     = "Magreza"
    NORMAL      = "Normal"
    SOBREPESO   = "Sobrepeso"
    OBESIDADE_1 = "Obesidade"
    OBESIDADE_2 = "Obesidade Grave"
    
def calculateIMC(weight, height):
    return round(weight/height ** 2, 2)

def statusByIMC(imc):
    match imc:
        case _ if imc < 18.5:
            return Status.MAGREZA
        case _ if 18.5 <= imc < 25:
            return Status.NORMAL
        case _ if 25 <= imc < 30:
            return Status.SOBREPESO
        case _ if 30 <= imc < 40:
            return Status.OBESIDADE_1
        case _ if imc >= 40:
            return Status.OBESIDADE_2
        
imc = calculateIMC(a_weight, a_height)
status = statusByIMC(imc)        

print(f"IMC: {imc} - Status: {status}")
