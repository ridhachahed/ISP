import asyncio
import websockets
import hashlib
import os

EMAIL = "mohamed.chahed@epfl.ch"
PASSWORD = "correct horse battery staple"
#H = sha256 ??
N = "EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3"
g = 2
size = 32

async def pake(websocket, path):

    email_utf8_hex = format(EMAIL, "x").encode()
    await websocket.send(email_utf8_hex)
    #hash.update(utf8_hex)

    # Number is received as UTF-8 encoded hexadecimal String
    salt_utf8_hex = await websocket.recv()

    # Hexadecimal string is converted back to an integer
    salt_integer = int(salt_utf8_hex, 16)

    random_bytes = os.urandom(size)
    a = int.from_bytes(random_bytes)
    n_int = int(N, 16)
    A = pow(g, a, n_int)

    b_utf8_hex = await websocket.recv()

    # u = H(A || B)
    u = hashlib.sha256()
    u.update(format(A, "x").encode())
    u.update(b_utf8_hex)
    # digest() returns an hexadecimal representation of the hash
    U = u.digest()

    # x = H(salt || H(U || ":" || PASSWORD))
    x = hashlib.sha256()
    x.update(salt_utf8_hex)

    # y = H(U || ":" || PASSWORD)
    # x = H(salt || Y)
    y = hashlib.sha256()
    y.update(U.encode())
    y.update(format(':', "x").encode())
    y.update(format(PASSWORD, "x").encode())
    Y = y.digest()

    x.update(Y.encode())

    # doubts on encode here
    x_integer = int(x.digest().encode(), 16)

    # S = (B - g ^ x) ^ (a + u * x) % N
    B = int(b_utf8_hex,16)

    S = pow(B - g ** x_integer, a + u * x_integer)

    await websocket.send(S)

start_server = websockets.serve(pake, "ws://127.0.0.1:/", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

