import streamlit as st

def main():
    st.title("PRESENT Şifreleme Aracı")

    # Anahtar ve metin girişi
    key = st.text_input("Anahtar (hexadecimal)", "0123456789ABCDEF0123")
    plaintext = st.text_input("Şifrelenecek Metin (hexadecimal)", "0123456789ABCDEF")

    if st.button("Şifrele"):
        # Hexadecimal'den integer'a dönüştürme
        key_int = int(key, 16)
        plaintext_int = int(plaintext, 16)

        # Şifreleme
        ciphertext = present_encrypt(plaintext_int, key_int)
        st.write("Şifreli Metin:", hex(ciphertext))

    if st.button("Deşifre Et"):
        # Hexadecimal'den integer'a dönüştürme
        ciphertext_int = int(plaintext, 16)

        # Deşifreleme
        decrypted_text = present_decrypt(ciphertext_int, key_int)
        st.write("Deşifre Edilen Metin:", hex(decrypted_text))

if __name__ == "__main__":
    main()
