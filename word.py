import re
from collections import Counter

def read_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sentences = file.readlines()
    return sentences

def preprocess_sentences(sentences):
    # Удаление символов новой строки и лишних пробелов
    sentences = [sentence.strip() for sentence in sentences]

    # Добавление маркеров начала и конца предложения
    sentences = ['<start> ' + sentence + ' <end>' for sentence in sentences]

    # Разделение предложений на токены с сохранением информации о знаках препинания
    tokenized_sentences = [re.findall(r"[\w']+|[.,!?;]", sentence) for sentence in sentences]

    return tokenized_sentences

def create_vocab(tokenized_sentences):
    # Создание словаря с частотой слов (токенов) в корпусе
    word_freq = Counter([word for sentence in tokenized_sentences for word in sentence])

    # Сортировка слов по убыванию частоты
    sorted_words = sorted(word_freq, key=word_freq.get, reverse=True)

    # Добавление специальных маркеров начала и конца предложения
    special_tokens = ['<pad>', '<start>', '<end>', '<unk>']
    sorted_words = special_tokens + sorted_words

    # Создание словаря, преобразующего слова (токены) в числовые идентификаторы
    word_to_id = {word: idx for idx, word in enumerate(sorted_words)}

    # Создание обратного словаря для декодирования
    id_to_word = {idx: word for word, idx in word_to_id.items()}

    return word_to_id, id_to_word


file_path = "merged.txt"
sentences = read_sentences(file_path)
tokenized_sentences = preprocess_sentences(sentences)

word_to_id, id_to_word = create_vocab(tokenized_sentences)
# print(word_to_id)