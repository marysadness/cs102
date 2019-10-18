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
        if (ord('a') <= j <= ord('z')) or (ord('A') <= j <= ord('Z')):
            if (ord('a') <= j <= ord('w')) or (ord('A') <= j <= ord('W')):
                h = chr(j + 3)
            else:
                h = chr(j - 23)
        ciphertext = ciphertext + h

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
        if (ord('a') <= t <= ord('z')) or (ord('A') <= t <= ord('Z')):
            if (ord('d') <= t <= ord('z')) or (ord('D') <= t <= ord('Z')):
                u = chr(t - 3)
            else:
                u = chr(t + 23)
        plaintext += u
    return plaintext
