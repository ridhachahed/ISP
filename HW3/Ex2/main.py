import hashlib
import pickle

ROWS = 10 * pow(10, 6)
COLS = pow(10, 3)

def reduction(hash,col):
    hash = hash + col
    charset = list('abcdefghijklmnopqrstuvwxyz0123456789')
    p = ''
    for _ in range(8):
        r = hash % 36
        p = p + charset[r]
        hash = hash // 36

    return p

def generate_table():
    dictionary = {}
    for row in range(ROWS):
        p_init = reduction(row, 0)
        h = hashlib.sha256(p_init.encode()).hexdigest()
        h_int = int(h,16)

        for col in range(1,COLS):
            p = reduction(h_int, col)
            h = hashlib.sha256(p.encode()).hexdigest()
            h_int = int(h,16)

        dictionary[p_init] = h
    print('Table computed')

    # Store data (serialize)
    with open('rainbow_table.pickle', 'wb') as handle:
        pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return dictionary

#hash is in HEX
def attack(hash,generate = False):

    if generate:
        dictionary = generate_table()

    else:

        file_to_read = open("rainbow_table.pickle", "rb")
        dictionary = pickle.load(file_to_read)

        last_hashes = set(dictionary.values())

        #first verify if hash is not in the last_hashes
        if hash in last_hashes:

            # list out keys and values separately
            key_list = list(dictionary.keys())
            val_list = list(dictionary.values())

            p_init = key_list[val_list.index(hash)]

            h = hashlib.sha256(p_init.encode()).hexdigest()
            h_int = int(h, 16)

            for col in range(1, COLS):
                p = reduction(h_int, col)
                h = hashlib.sha256(p.encode()).hexdigest()
                h_int = int(h, 16)
            return p

        else :
            # if not need to apply the last reduction and apply a hash and verify again
            for col_end in range(1,COLS,-1):
                h_int = int(hash,16)
                for col in range(col_end,COLS):
                    p = reduction(h_int, col)
                    h = hashlib.sha256(p.encode()).hexdigest()
                    h_int = int(h, 16)



if __name__ == '__main__':

