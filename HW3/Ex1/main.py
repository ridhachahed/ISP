import pickle
from multiprocessing import Pool
import hashlib
from itertools import chain, product

HASHES1 = ['7c58133ee543d78a9fce240ba7a273f37511bfe6835c04e3edf66f308e9bc6e5',
           '37a2b469df9fc4d31f35f26ddc1168fe03f2361e329d92f4f2ef04af09741fb9',
           '19dbaf86488ec08ba7a824b33571ce427e318d14fc84d3d764bd21ecb29c34ca',
           '06240d77c297bb8bd727d5538a9121039911467c8bb871a935c84a5cfe8291e4',
           'f5cd3218d18978d6e5ef95dd8c2088b7cde533c217cfef4850dd4b6fa0deef72',
           'dd9ad1f17965325e4e5de2656152e8a5fce92b1c175947b485833cde0c824d64',
           '845e7c74bc1b5532fe05a1e682b9781e273498af73f401a099d324fa99121c99',
           'a6fb7de5b5e11b29bc232c5b5cd3044ca4b70f2cf421dc02b5798a7f68fc0523',
           '1035f3e1491315d6eaf53f7e9fecf3b81e00139df2720ae361868c609815039c',
           '10dccbaff60f7c6c0217692ad978b52bf036caf81bfcd90bfc9c0552181da85a']

HASHES2 = ['2e41f7133fd134335f566736c03cc02621a03a4d21954c3bec6a1f2807e87b8a',
           '7987d2f5f930524a31e0716314c2710c89ae849b4e51a563be67c82344bcc8da',
           '076f8c265a856303ac6ae57539140e88a3cbce2a2197b872ba6894132ccf92fb',
           'b1ea522fd21e8fe242136488428b8604b83acea430d6fcd36159973f48b1102e',
           '3992b888e772681224099302a5eeb6f8cf27530f7510f0cce1f26e79fdf8ea21',
           '326e90c0d2e7073d578976d120a4071f83ce6b7bc89c16ecb215d99b3d51a29b',
           '269398301262810bdf542150a2c1b81ffe0e1282856058a0e26bda91512cfdc4',
           '4fbee71939b9a46db36a3b0feb3d04668692fa020d30909c12b6e00c2d902c31',
           '55c5a78379afce32da9d633ffe6a7a58fa06f9bbe66ba82af61838be400d624e',
           '5106610b8ac6bc9da787a89bf577e888bce9c07e09e6caaf780d2288c3ec1f0c']

HASHES3 = ['962642e330bd50792f647c1bf71895c5990be4ebf6b3ca60332befd732aed56c',
           '8eef79d547f7a6d6a79329be3c7035f8e377f9e629cd9756936ec233969a45a3',
           'e71067887d50ce854545afdd75d10fa80b841b98bb13272cf4be7ef0619c7dab',
           '889a22781ef9b72b7689d9982bb3e22d31b6d7cc04db7571178a4496dc5ee128',
           '6a16f9c6d9542a55c1560c65f25540672db6b6e121a6ba91ee5745dabdc4f208',
           '2317603823a03507c8d7b2970229ee267d22192b8bb8760bb5fcef2cf4c09edf',
           'c6c51f8a7319a7d0985babe1b6e4f5c329403d082e05e83d7b9d0bf55876ecdc',
           'c01304fc36655dd37b5aa8ca96d34382ed9248b87650fffcd6ec70c9342bf451',
           'cff39d9be689f0fc7725a43c3bdc7f5be012c840b9db9b547e6e3c454a076fc8',
           '662ab7be194cee762494c6d725f29ef6321519035bfb15817e84342829728891']

SALTS3 = ['b9', 'be', 'bc', '72', '9f', '17', '94', '7f', '2e', '24']


def encrypt_string(word):
    sha_signature = \
        hashlib.sha256(word.encode()).hexdigest()
    return word, sha_signature


# generated from the set of lowercase letters and digits (‘abcd. . . xyz0123. . . 9’)
# have length 4, 5,or 6 characters
def bruteforce_attack():
    charset = 'abcdefghijklmnopqrstuvwxyz0123456789'

    # chain transforms several iterables into 1
    # product is cross product like several for loops

    dictionary = (''.join(candidate)
                  for candidate in chain.from_iterable(product(charset, repeat=i)
                                                       for i in range(4, 6 + 1)))
    cracked_pwd = {}
    with Pool(5) as pool:

        for word, encryption in pool.imap_unordered(encrypt_string, dictionary):

            if encryption in HASHES1:
                cracked_pwd[encryption] = word

                print('Password ' + encryption + ' cracked !')
                print('Password is : ' + word)

    file_save = open("pwd_craked_brute_force.pkl", "wb")
    pickle.dump(cracked_pwd, file_save)
    file_save.close()


def read_dictionaries():
    # dictionaries downloaded from https://wiki.skullsecurity.org/Passwords
    files = ['rockyou.txt', '500-worst-passwords.txt', 'cain.txt', 'conficker.txt', 'john.txt', 'twitter-banned.txt']
    words = []
    for name in files:
        with open('Dictionaries/' + name, encoding='latin-1') as f:
            words += f.read().splitlines()

    print("We use {0} dictionaries and we have {1} words".format(len(files), len(words)))
    return words


def modif_pipeline(word, rule1, rule2, rule3, rule4):
    # Rule 1
    # capitalise the first letter and every letter which comes after a digit
    if rule1:
        word = word.title()

    # Rule 2
    # change ‘e’ to ‘3’
    if rule2 and 'e' in word.lower():
        word = word.replace('e', '3')
        word = word.replace('E', '3')

    # Rule 3
    # change ‘o’ to ‘0’
    if rule3 and 'o' in word.lower():
        word = word.replace('o', '0')
        word = word.replace('O', '0')

    # Rule 4
    # change ‘i’ to ‘1’
    if rule4 and 'i' in word.lower():
        word = word.replace('i', '1')
        word = word.replace('I', '1')

    return word


def modify_encrypt(word):
    possible_modifications = set()

    for rules in product([True, False], repeat=4):
        possible_modifications.add(modif_pipeline(word, *rules))

    return possible_modifications


def dictionary_attack():
    dictionary = read_dictionaries()

    cracked_pwd = {}

    with Pool(5) as pool:
        for modifs in pool.imap_unordered(modify_encrypt, dictionary):

            for modif in modifs:
                encryption = hashlib.sha256(modif.encode()).hexdigest()

                if encryption in HASHES2:
                    cracked_pwd[encryption] = modif

                    print('Password ' + encryption + ' cracked !')
                    print('Password is : ' + modif)

    file_save = open("pwd_craked_dictionary.pkl", "wb")
    pickle.dump(cracked_pwd, file_save)
    file_save.close()

def salted_dictionary_attack():

    dictionary = read_dictionaries()

    cracked_pwd = {}

    with Pool(5) as pool:
        for modifs in pool.imap_unordered(modify_encrypt, dictionary):

            for modif in modifs:

                for salt, hash in zip(SALTS3, HASHES3):
                    modif_salted = modif + salt
                    encryption = hashlib.sha256(modif_salted.encode()).hexdigest()
                    if(encryption == hash):
                        cracked_pwd[encryption] = modif

                        print('Password ' + encryption + ' cracked !')
                        print('Password is : ' + modif)

    file_save = open("pwd_craked_salted_dictionary.pkl", "wb")
    pickle.dump(cracked_pwd, file_save)
    file_save.close()

if __name__ == '__main__':
    print("Brute force attack:")
    bruteforce_attack()

    print("Dictionary attack:")
    dictionary_attack()

    print("Salted dictionary attack")
    salted_dictionary_attack()
