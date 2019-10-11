def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    for i in range(len(plaintext)):
        position = ord(plaintext[i])
        h = plaintext[i]
        g = len(keyword)
        if ord(keyword[i % g]) >= ord('a') and ord(keyword[i % g]) <= ord('z'):
            k = ord(keyword[i % g]) - ord('a')
        else:
            k = ord(keyword[i % g]) - ord('A')
        k = k % 26
        if (position >= ord('a') and position <= ord('z')):
            z = ord('z')
            a = ord('a')
            if position + k > z:
                h = chr(k - (z - position) + a - 1)
            else:
                h = chr(k + position)
        elif (position >= ord('A') and position <= ord('Z')):
            z = ord('Z')
            a = ord('A')
            if position + k > z:
                h = chr(k - (z - position) + a - 1)
            else:
                h = chr(k + position)
        ciphertext += h
    return ciphertext

def decrypt_vigenere(siphertext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    plaintext = ''
    for i in range(len(siphertext)):
        position = ord(siphertext[i])
        h = siphertext[i]
        g = len(keyword)
        if ord(keyword[i % g]) >= ord('a') and ord(keyword[i % g]) <= ord('z'):
            k = ord(keyword[i % g]) - ord('a')
        else:
            k = ord(keyword[i % g]) - ord('A')
        k = k % 26
        if (position >= ord('a') and position <= ord('z')):
            z = ord('z')
            a = ord('a')
            if position - k < a:
                h = chr(z - (k - (position - a)))
            else:
                h = chr(position - k)
        elif (position >= ord('A') and position <= ord('Z')):
            z = ord('Z')
            a = ord('A')
            if position - k > a:
                h = chr(z - (k - (position - a)))
            else:
                h = chr(position - k)
        plaintext += h


    return plaintext