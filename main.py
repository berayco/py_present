# S-box ve P-box tanımlamaları
SBOX = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]
PBOX = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51, 4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55, 8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59, 12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]

def sbox_layer(state, sbox):
    new_state = 0
    for i in range(16):
        nibble = (state >> (i * 4)) & 0xF
        new_state |= sbox[nibble] << (i * 4)
    return new_state

def pbox_layer(state, pbox):
    new_state = 0
    for i in range(64):
        bit = (state >> i) & 0x1
        new_state |= bit << pbox[i]
    return new_state

def key_schedule(master_key):
    subkeys = [master_key >> 16]
    for i in range(1, 32):
        master_key = ((master_key & 0xFFFF) << 60) | (master_key >> 20)
        master_key = (sbox_layer(master_key >> 76, SBOX) << 76) | (master_key & ((1 << 76) - 1))
        master_key ^= i << 15
        subkeys.append(master_key >> 16)
    return subkeys

def present_encrypt(plaintext, master_key):
    keys = key_schedule(master_key)
    state = plaintext
    for i in range(31):
        state = sbox_layer(state ^ keys[i], SBOX)
        state = pbox_layer(state, PBOX)
    return state ^ keys[31]

def present_decrypt(ciphertext, master_key):
    keys = key_schedule(master_key)
    state = ciphertext
    for i in range(31, 0, -1):
        state = sbox_layer(state ^ keys[i], [SBOX.index(x) for x in range(16)])
        state = pbox_layer(state, [PBOX.index(x) for x in range(64)])
    return state ^ keys[0]

# Streamlit arayüzü
import streamlit as st

def main():
    st.title('PRESENT Şifreleme Algoritması')

    plaintext = st.text_input('Düz Metin (hex):')
    key = st.text_input('Anahtar (hex):')

    if st.button('Şifrele'):
        pt = int(plaintext, 16)
        k = int(key, 16)
        ct = present_encrypt(pt, k)
        st.write(f'Şifreli Metin: {ct:016x}')

    if st.button('Şifre Çöz'):
        ct = int(plaintext, 16)
        k = int(key, 16)
        pt = present_decrypt(ct, k)
        st.write(f'Çözülmüş Metin: {pt:016x}')

if __name__ == '__main__':
    main()
