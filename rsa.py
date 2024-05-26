import random
import json
from sympy import isprime, mod_inverse


# Функция для генерации простых чисел
def generate_prime_candidate(length):
    p = 0
    while not isprime(p):
        p = random.getrandbits(length)
    return p


# Функция для генерации ключей
def generate_keys(keysize=1024):
    e = d = n = 0

    p = generate_prime_candidate(keysize // 2)
    q = generate_prime_candidate(keysize // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Найти e такой, чтобы 1 < e < phi и gcd(e, phi) = 1; обычно берется 65537
    e = 65537
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    # Найти d
    d = mod_inverse(e, phi)

    # Публичный и приватный ключи
    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key


# Функция для вычисления gcd
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# Функция для шифрования
def encrypt(plaintext, public_key):
    e, n = public_key
    ciphertext = [pow(ord(char), e, n) for char in plaintext]
    return ciphertext


# Функция для расшифрования
def decrypt(ciphertext, private_key):
    d, n = private_key
    plaintext = ''.join([chr(pow(char, d, n)) for char in ciphertext])
    return plaintext


# Функция для записи ключей в файл
def save_keys(public_key, private_key, filename='keys.json'):
    keys = {
        'public_key': public_key,
        'private_key': private_key
    }
    with open(filename, 'w') as f:
        json.dump(keys, f)


# Функция для чтения ключей из файла
def load_keys(filename='keys.json'):
    with open(filename, 'r') as f:
        keys = json.load(f)
        public_key = tuple(keys['public_key'])
        private_key = tuple(keys['private_key'])
        return public_key, private_key


# Основная функция
def main():
    print("1. Генерировать ключевую пару")
    print("2. Зашифровать файл")
    print("3. Расшифровать файл")
    choice = input("Выберите опцию (1/2/3): ")

    if choice == '1':
        keysize = int(input("Введите размер ключа (в битах): "))
        public_key, private_key = generate_keys(keysize)
        save_keys(public_key, private_key)
        print(f"Ключевая пара сгенерирована и сохранена в 'keys.json'")

    elif choice == '2':
        filename = input("Введите имя файла для шифрования: ")
        with open(filename, 'r') as f:
            plaintext = f.read()

        public_key, _ = load_keys()
        ciphertext = encrypt(plaintext, public_key)

        output_filename = filename + '.enc'
        with open(output_filename, 'w') as f:
            f.write(' '.join(map(str, ciphertext)))

        print(f"Файл зашифрован и сохранен как '{output_filename}'")

    elif choice == '3':
        filename = input("Введите имя файла для расшифрования: ")
        with open(filename, 'r') as f:
            ciphertext = list(map(int, f.read().split()))

        _, private_key = load_keys()
        plaintext = decrypt(ciphertext, private_key)

        output_filename = filename + '.dec'
        with open(output_filename, 'w') as f:
            f.write(plaintext)

        print(f"Файл расшифрован и сохранен как '{output_filename}'")

    else:
        print("Неправильный выбор")


if __name__ == '__main__':
    main()
