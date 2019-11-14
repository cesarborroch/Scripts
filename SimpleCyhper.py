# Shifts a text 13 letters to the right

def cipher(string):
    result = ''

    alphabet = 'abcdefghijklmnopqrstuvwxyzabcdefghijklm'

    for letter in string.lower():

        if letter in alphabet:
            result += alphabet[alphabet.index(letter) + 13]
        else:
            result += letter

    return result

print(cipher("I was born 10,000 years ago."))

