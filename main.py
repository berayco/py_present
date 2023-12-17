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
    round_keys = key_schedule(key, 80)
    state = plaintext
    for round_key in round_keys:
        state ^= round_key
        state = substitute(state, SBOX)
        state = permute(state, PBOX)
    return state

def decrypt(ciphertext, key):
    """ Şifre çözme işlevi """
    round_keys = key_schedule(key, 80)
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

# Şifreleme Bölümü
st.header("Şifreleme")
key_input = st.text_input("Anahtar (hexadecimal) - Şifreleme", "00000000000000000001")
plaintext_input = st.text_input("Düz Metin (hexadecimal) - Şifreleme", "0000000000000001")

try:
    key = int(key_input, 16)
    plaintext = int(plaintext_input, 16)
    if st.button("Şifrele"):
        ciphertext = encrypt(plaintext, key)
        st.text_area("Şifreli Metin", f"{ciphertext:016x}", height=100)
except ValueError:
    st.error("Lütfen geçerli bir hexadecimal değer giriniz.")

# Şifre Çözme Bölümü
st.header("Şifre Çözme")
key_input_decrypt = st.text_input("Anahtar (hexadecimal) - Şifre Çözme", "00000000000000000001")
ciphertext_input = st.text_input("Şifreli Metin (hexadecimal) - Şifre Çözme")

try:
    key_decrypt = int(key_input_decrypt, 16)
    ciphertext = int(ciphertext_input, 16)
    if st.button("Şifre Çöz"):
        decrypted_text = decrypt(ciphertext, key_decrypt)
        st.text_area("Çözülmüş Metin", f"{decrypted_text:016x}", height=100)
except ValueError:
    st.error("Lütfen geçerli bir hexadecimal değer giriniz.")

# Uygulamayı çalıştırmak için terminalde 'streamlit run [dosya_adı].py' komutunu kullanın.
