# Discovers passwords that contains only letters and numbers
# Add more symbols to string digits as needed

def toPassword(dec):
    digits = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    x = int((dec % len(digits))) - 1
    rest = int(dec / len(digits))
    if (rest == 0):
        return digits[x]
    return toPassword(rest) + digits[x]

password = 'pass123'

attempt = 0;

while password != toPassword(attempt):
    # Imprime 1 tentativa a cada meio milhao
    if(attempt % 500000 == 0):
        print(toPassword(attempt))
    attempt += 1

print('Password found is "{}", after {} attempts.'.format(toPassword(attempt), attempt))
