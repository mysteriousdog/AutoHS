import itertools
import string

def generate_variants(email):
    username, domain = email.split('@')
    variants = set()
    for i in range(len(username)):
        if username[i] in string.ascii_letters:
            variants.add(username[:i] + username[i].lower() + username[i+1:])
            variants.add(username[:i] + username[i].upper() + username[i+1:])
    return [v + '@' + domain for v in variants]


def generate_emails(email):
    username, domain = email.split('@')
    username = username.replace('.', '')
    variations = []
    for i in range(1, len(username) + 1):
        for combination in itertools.combinations(range(len(username)), i):
            new_username = list(username)
            for index in combination:
                new_username[index] = '.' + new_username[index]
            variations.append(''.join(new_username))
    return [variation + '@' + domain for variation in variations]

email = input('Enter a Gmail email: ')
emails = generate_emails(email)
a = []
for email in emails:
    a += generate_variants(email)

print(len(a))
passwd = input('Enter a passwd: ')
for b in a:
    print(b, " ", passwd)



