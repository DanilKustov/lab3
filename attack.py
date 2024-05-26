# Функция для вычисления НОД
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Функция для вычисления мультипликативного обратного
def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

# Функция для факторизации числа n
def factorize_n(n):
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return i, n // i
    return None, None

# Функция для расшифрования
def decrypt(ciphertext, private_key):
    d, n = private_key
    plaintext = ''.join([chr(pow(char, d, n)) for char in ciphertext])
    return plaintext

# Пример значений (используем малые значения для демонстрации)
p = 61
q = 53
n = p * q
phi = (p - 1) * (q - 1)
e = 17
d = mod_inverse(e, phi)

# Открытый и закрытый ключи
public_key = (e, n)
private_key = (d, n)

# Сообщение для шифрования
message = "Hello world"
ciphertext = [pow(ord(char), e, n) for char in message]

print("Зашифрованное сообщение:", ciphertext)

# Атака на RSA
# 1. Факторизация n
p_factored, q_factored = factorize_n(n)
if p_factored and q_factored:
    print(f"Факторизация успешна: p = {p_factored}, q = {q_factored}")
    # 2. Вычисление phi(n)
    phi_factored = (p_factored - 1) * (q_factored - 1)
    # 3. Вычисление закрытого ключа d
    d_factored = mod_inverse(e, phi_factored)
    # 4. Расшифрование сообщения
    private_key_factored = (d_factored, n)
    decrypted_message = decrypt(ciphertext, private_key_factored)
    print("Расшифрованное сообщение:", decrypted_message)
else:
    print("Факторизация не удалась")
