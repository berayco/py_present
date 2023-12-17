import streamlit as st

# PRESENT Şifreleme Algoritması İşlevleri

def key_schedule(key, key_size):
    """ Anahtar zamanlaması işlevi """
    round_keys = []
    for round in range(1, 32):
        round_keys.append(key >> (key_size - 64))
        key = ((key & (2**(key_size - 19) - 1)) << 19) | (key >> (key_size - 19))
        top_four = (key >> (key_size - 4)) & 0xF
        key ^= (SBOX[top_four] << (key_size - 4))
        key ^= ((round & 1) << 15)
        key ^= ((round >> 4) & 1) << 4
        key ^= ((round >> 4) & 1) << 63
    return round_keys

def substitute(state, sbox):
    """ Substitüsyon işlevi """
    substituted = 0
    for i in range(16):
        substituted |= sbox[(state >> (i * 4)) & 0xF] << (i * 4)
    return substituted

def permute(state, pbox):
    """ Permütasyon işlevi """
    permuted = 0
    for i in range(64):
        permuted |= ((state >> i) & 1) << pbox[i]
    return permuted

def encrypt(plaintext, key):
    """ Şifreleme işlevi """
    round_keys = key_schedule(key, len(bin(key)) - 2)
    state = plaintext
    for round_key in round_keys:
        state ^= round_key
        state = substitute(state, SBOX)
        state = permute(state, PBOX)
    return state

def decrypt(ciphertext, key):
    """ Şifre çözme işlevi """
    round_keys = key_schedule(key, len(bin(key)) - 2)
    state = ciphertext
    for round_key in reversed(round_keys):
        state = permute(state, INVERSE_PBOX)
        state = substitute(state, INVERSE_SBOX)
        state ^= round_key
    return state

# S-Box, Ters S-Box, P-Box ve Ters P-Box Tanımlamaları
SBOX = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]
INVERSE_SBOX = [SBOX.index(x) for x in range(16)]
PBOX = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51,
        4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55,
        8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59,
        12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]
INVERSE_PBOX = [PBOX.index(x) for x in range(64)]

# Streamlit Arayüzü
st.title("PRESENT Şifreleme ve Şifre Çözme Algoritması")

# Kullanıcı girdileri
key_input = st.text_input("Anahtar (hexadecimal)", "00000000000000000001")
plaintext_input = st.text_input("Düz Metin (hexadecimal)", "0000000000000001")

# Girdileri integer'a çevir
key = int(key_input, 16)
plaintext = int(plaintext_input, 16)

if st.button("Şifrele"):
    ciphertext = encrypt(plaintext, key)
    st.write(f"Şifreli Metin: {ciphertext:016x}")

if st.button("Şifre Çöz"):
    ciphertext_input = st.text_input("Şifreli Metin (hexadecimal)")
    if ciphertext_input:
        ciphertext = int(ciphertext_input, 16)
        decrypted_text = decrypt(ciphertext, key)
        st.write(f"Çözülmüş Metin: {decrypted_text:016x}")

# Uygulamayı çalıştırmak için terminalde 'streamlit run [dosya_adı].py' komutunu kullanın.
