def encrypt_caesar(plaintext: str) -> str:
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ''
    for i in range(len(plaintext)):
        h = plaintext[i]  # символ
        j = ord(plaintext[i])  # номер позиции символа
        if (j >= ord('a') and j <= ord('w')) or (j >= ord('A') and j <= ord('W')):
            h = chr(j + 3)
        elif (j >= ord('x') and j <= ord('z')):
            z = ord('z')
            r1 = ord('a')
            r1 = r1 + z - j
            h = chr(r1)
        elif (j >= ord('X') and j <= ord('Z')):
            z = ord('Z')
            r1 = ord('A')
            r1 = r1 + z - j
            h = chr(r1)
        ciphertext += h
    return ciphertext


def decrypt_caesar(ciphertext: str) -> str:
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """


    plaintext = ''
    for i in range(len(ciphertext)):
        u = ciphertext[i]  # символ
        t = ord(ciphertext[i])
        if (t >= ord('d') and t <= ord('z')) or (t >= ord('D') and t <= ord('Z')):
            u = chr(t - 3)
        elif (t >= ord('a') and t <= ord('c')):
            z = ord('z')
            r1 = ord('a')
            r1 = z -(t - r1)
            u = chr(r1)
        elif (t >= ord('A') and t <= ord('C')):
            z = ord('Z')
            r1 = ord('A')
            r1 = z -(t - r1)
            u = chr(r1)
        plaintext += u
    return plaintext


    return plaintext