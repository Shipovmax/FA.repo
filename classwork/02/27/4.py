class CipherMaster:
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

    def process_text(self, text, shift, is_encrypt):
        text = text.lower()
        if not is_encrypt:
            shift = -shift

        result = []
        for char in text:
            if char in self.alphabet:
                index = self.alphabet.find(char)
                new_index = (index + shift) % len(self.alphabet)
                result.append(self.alphabet[new_index])
            else:
                result.append(char)
        return "".join(result)


# Проверка
cipher_master = CipherMaster()
print(
    cipher_master.process_text(
        text="Однажды ревьюер принял проект с первого раза, с тех пор я его боюсь",
        shift=2,
        is_encrypt=True,
    )
)
print(
    cipher_master.process_text(
        text="Олебэи яфвнэ мроплж сэжи — э пэй рдв злййвкпш лп нвящывнэ",
        shift=-3,
        is_encrypt=False,
    )
)
