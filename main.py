import streamlit as st

# S-box ve P-box tanımlamaları
SBOX = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]
INVERSE_SBOX = [SBOX.index(x) for x in range(16)]
PBOX = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51, 4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55, 8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59, 12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]
INVERSE_PBOX = [PBOX.index(x) for x in range(64)] # P-Box tersi

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
    keys.reverse() # Anahtarların sırasını tersine çevir
    state = ciphertext
    for i in range(31, 0, -1):
        state = sbox_layer(state ^ keys[i], INVERSE_SBOX)
        state = pbox_layer(state, INVERSE_PBOX)
    return state ^ keys[0]

def present_page():
    st.header('PRESENT Şifreleme Algoritması')

    # Kullanıcıdan metin alın
    input_text = st.text_input('Şifrelenecek Metin (Hex):', '1234567890ABCDEF')
    # Sabit bir anahtar kullan
    fixed_key = 0x0123456789ABCDEFFEDCBA9876543210

    if st.button('Şifrele ve Şifre Çöz'):
        if input_text and all(c in '0123456789abcdefABCDEF' for c in input_text):
            try:
                input_val = int(input_text, 16)
                encrypted = present_encrypt(input_val, fixed_key)
                decrypted = present_decrypt(encrypted, fixed_key)

                st.write(f"Şifrelenmiş Metin: {encrypted:016x}")
                st.write(f"Çözülmüş Metin: {decrypted:016x}")

                if input_val == decrypted:
                    st.write("Şifreleme ve Şifre Çözme Başarılı!")
                else:
                    st.write("Şifreleme ve Şifre Çözme Başarısız.")
            except Exception as e:
                st.write(f"Bir hata oluştu: {e}")
        else:
            st.write('Lütfen geçerli bir metin girin (hex formatında).')

def main():
    st.title('PRESENT Şifreleme Algoritması Testi')
    present_page()

if __name__ == '__main__':
    main()
