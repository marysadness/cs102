def encrypt_caesar(plaintext: str):
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
    ciphertext = plaintext
    for i in range(k):
        f = plaintext[i] #символ
        h = f #симыол, который при необходимости будет изменяться
        j = ord(plaintext[i]) #номер позиции символа
        if (j >= ord('a') and j <= ord('z')) or (j >= ord('A') and j <= ord('Z')):
            if (j >= ord('d') and j <= ord('z')) or (j >= ord('D') and j <= ord('Z')):
                h = chr(position - 3)
                plaintext = plaintext.replace(f, h)
            else:
                if j <= ord('d'):
                    x = ord('x')
                    r = ord('')
                elif j <= ord('D'):
                    x = ord('X')
                    r = ord('A')
                r = position - r + x
                h = chr(r)
        ciphertext = plaintext.replace(f, h)


    return ciphertext


def encrypt_caesar(ciphertext):
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
	for i in range(k):
		plaintext = ciphertext
		position = ord(ciphertext[i]) #номер позиции символа
		p = chr(position) #символ
		u = p #симыол, который при необходимости будет изменяться
	    if (ord(ciphertext[i]) >= ord('a') and ord(ciphertext[i]) <= ord('z')) or (ord(ciphertext[i]) >= ord('A') and ord(ciphertext[i]) <= ord('Z')):
			if (ord(ciphertext[i]) >= ord('d')) or (ord(ciphertext[i]) >= ord('D')):
			    position = ord(ciphertext[i])
		        u = chr(position - 3)
		        p = chr(position)
                plaintext = ciphertext.replace(p, u)
		else:
			if ord(ciphertext[i]) <= ord('d'):
			    position = ord(ciphertext[i])
			    a = ord('a')
			    r = ord('x') + (position - a)
			    u = chr(r)
            else:
                position = ord(ciphertext[i])
			    a = ord('A')
			    r = ord('X') + (position - a)
			    u = chr(r)
		    p = chr(position)
	    plaintext = ciphertext.replace(p, u)
	return plaintext