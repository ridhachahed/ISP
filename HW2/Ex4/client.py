import asyncio
import websockets
import hashlib
import os

EMAIL = "mohamed.chahed@epfl.ch"
PASSWORD = "correct horse battery staple"
N = "EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3"
g = 2
size = 32


async def pake():
    async with websockets.connect(
            'ws://127.0.0.1:5000') as websocket:

        # Send email UTF-8 encoded
        email_utf8 = EMAIL.encode()
        await websocket.send(email_utf8)
        print("Email sent : " + EMAIL)

        # Salt is received as UTF-8 encoded hexadecimal String
        salt_utf8_hex = await websocket.recv()

        # Hexadecimal string is converted back to an integer
        salt_integer = int(salt_utf8_hex, 16)

        print("Salt received:" + str(salt_integer))

        # generate 32 random bytes
        random_bytes = os.urandom(size)
        # generate integer form bytes
        a = int.from_bytes(random_bytes, 'big')
        n_int = int(N, 16)
        A = pow(g, a, n_int)

        print("A computed : " + str(A))

        # send A as UTF-8 encoded hexadecimal String to server
        a_utf8_hex = format(A, "x").encode()

        await websocket.send(a_utf8_hex)

        # B is received as UTF-8 encoded hexadecimal String
        b_utf8_hex = await websocket.recv()

        print(b_utf8_hex)

        # u = H(A || B)
        u = hashlib.sha256()
        u.update(a_utf8_hex)
        u.update(b_utf8_hex.encode())

        # hexdigest() returns an hexadecimal representation of the hash
        u_integer = int(u.hexdigest(), 16)

        # x = H(salt || H(U || ":" || PASSWORD))
        x = hashlib.sha256()
        x.update(salt_utf8_hex.encode())

        # y = H(U || ":" || PASSWORD)
        # x = H(salt || Y)
        y = hashlib.sha256()
        y.update(EMAIL.encode())
        y.update(':'.encode())
        y.update(PASSWORD.encode())
        Y = y.hexdigest()

        x.update(Y.encode())

        x_integer = int(x.hexdigest(), 16)

        # S = (B - g ^ x) ^ (a + u * x) % N
        b_integer = int(b_utf8_hex, 16)

        S = pow(b_integer - g ** x_integer, a + u_integer * x_integer, n_int)

        print('S obtained :' +str(S))

        #send H(A || B || S)
        final_hash = hashlib.sha256()
        final_hash.update(a_utf8_hex)
        final_hash.update(b_utf8_hex.encode())
        final_hash.update(format(S, "x").encode())
        await websocket.send(final_hash)

        # get token
        token = await websocket.recv()
        print(token)

asyncio.get_event_loop().run_until_complete(pake())
