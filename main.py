import streamlit as st
def sbox(input_byte):
    SBOX = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]
    return SBOX[input_byte]

def inverse_sbox(input_byte):
    INV_SBOX = [0x5, 0xe, 0xf, 0x8, 0xC, 0x1, 0x2, 0xD, 0xB, 0x4, 0x6, 0x3, 0x0, 0x7, 0x9, 0xA]
    return INV_SBOX[input_byte]

def permute(state):
    PBOX = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51, 4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55, 8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59, 12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]
    permuted = 0
    for i in range(64):
        bit = (state >> i) & 1
        permuted |= bit << PBOX[i]
    return permuted

def inverse_permute(state):
    PBOX = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51, 4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55, 8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59, 12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]
    INV_PBOX = [PBOX.index(i) for i in range(64)]
    permuted = 0
    for i in range(64):
        bit = (state >> i) & 1
        permuted |= bit << INV_PBOX[i]
    return permuted

def key_schedule(key):
    subkeys = []
    for round in range(32):
        subkeys.append(key >> 16)
        key = ((key & 0xFFFF) << 60) | (key >> 20)
        key = (sbox(key >> 76) << 76) | (key & 0x0FFFFFFFFFFFFFFF)
        key ^= round << 15
    return subkeys

def present_encrypt(plaintext, key):
    subkeys = key_schedule(key)
    state = plaintext
    for i in range(31):
        state ^= subkeys[i]
        state = sum([sbox((state >> (4 * i)) & 0xF) << (4 * i) for i in range(16)])
        state = permute(state)
    state ^= subkeys[31]
    return state

def present_decrypt(ciphertext, key):
    subkeys = key_schedule(key)
    state = ciphertext
    for i in range(31, 0, -1):
        state ^= subkeys[i]
        state = inverse_permute(state)
        state = sum([inverse_sbox((state >> (4 * i)) & 0xF) << (4 * i) for i in range(16)])
    state ^= subkeys[0]
    return state

# Test
key = 0x00000000000000000001
plaintext = 0x1234567890abcdef
ciphertext = present_encrypt(plaintext, key)
decrypted = present_decrypt(ciphertext, key)

print(f"Plaintext:  {plaintext:016x}")
print(f"Ciphertext: {ciphertext:016x}")
print(f"Decrypted:  {decrypted:016x}")
st.title("PRESENT Şifreleme Algoritması")

operation = st.sidebar.selectbox("Mod Seçiniz", ["Şifreleme", "Şifre Çözme"])

key_input = st.text_input("Anahtar (Hexadecimal)", "00000000000000000001")
text_input = st.text_input(f"{operation} için Metin (Hexadecimal)")

if st.button(f"{operation}"):
    if text_input and key_input:
        try:
            key = int(key_input, 16)
            text = int(text_input, 16)
            if operation == "Şifreleme":
                result = present_encrypt(text, key)
            else:
                result = present_decrypt(text, key)
            st.write(f"Sonuç: {result:016x}")
        except ValueError:
            st.error("Lütfen geçerli hexadecimal değerler giriniz.")
    else:
        st.error("Lütfen gerekli alanları doldurunuz.")
