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
        f = plaintext[i] #символ
        h = f #симыол, который при необходимости будет изменяться
        j = ord(plaintext[i]) #номер позиции символа
        if (j >= ord('a') and j <= ord('w')) or (j >= ord('A') and j <= ord('W')):
            h = chr(j + 3)
        elif (j >= ord('x') and j <= ord('z')) or (j >= ord('X') and j <= ord('Z')):
            if j <= ord('Z'):
                z = ord('Z')
                r1 = ord('A')
            elif j <= ord('z'):
                z = ord('z')
                r1 = ord('a')
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
    plaintext = ""
    for i in range(len(ciphertext)):
        u = ciphertext[i]  # символ
        k = u  # симыол, который при необходимости будет изменяться
        t = ord(ciphertext[i])  # номер позиции символа
        if (t >= ord('d') and t <= ord('z')) or (t >= ord('D') and t <= ord('Z')):
            u = chr(t - 3)
        elif (t >= ord('a') and t <= ord('c')) or (t >= ord('A') and t <= ord('C')):
            if t <= ord('C'):
                c = ord('C')
                r2 = ord('Z')
            elif t <= ord('c'):
                c = ord('c')
                r2 = ord('z')
            r2 = r2 - (c - t)
            u = chr(r2)
        plaintext += u



    return plaintext
