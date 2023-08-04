import torch
import torch.nn as nn
from word import word_to_id, id_to_word
import torch.nn.functional as F
class TransformerModel(nn.Module):
    def __init__(self, vocab_size, d_model, nhead, num_encoder_layers, num_decoder_layers):
        super(TransformerModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.transformer = nn.Transformer(d_model=d_model, nhead=nhead, num_encoder_layers=num_encoder_layers,
                                          num_decoder_layers=num_decoder_layers)
        self.fc = nn.Linear(d_model, vocab_size)

    def forward(self, src, tgt):
        src_embed = self.embedding(src)
        tgt_embed = self.embedding(tgt)

        output = self.transformer(src_embed, tgt_embed)
        output = self.fc(output)

        return output

# Загрузка весов модели из файла
vocab_size = len(word_to_id)
d_model = 128
nhead = 8
num_encoder_layers = 4
num_decoder_layers = 4

model = TransformerModel(vocab_size, d_model, nhead, num_encoder_layers, num_decoder_layers)
model.load_state_dict(torch.load("transformer1_model.pth"))
model.eval()

# Функция для подготовки входных данных (пропустите этот шаг, если у вас уже есть функция preprocess_input)
def preprocess_input(input_data, word_to_id):
    input_ids = []
    for sentence in input_data:
        input_ids.append([word_to_id.get(word, word_to_id['<unk>']) for word in sentence])
    return torch.tensor(input_ids)

def generate_sentence(model, input_sentence, word_to_id, id_to_word, max_length=50):
    model.eval()
    input_tensor = preprocess_input([input_sentence], word_to_id)  # Convert the input sentence to tensor
    src = input_tensor.T

    tgt = torch.zeros_like(src)

    with torch.no_grad():
        for i in range(max_length):
            output = model(src, tgt)

            # Получаем вероятности для следующего токена с помощью softmax
            predicted_token_probs = F.softmax(output[-1, :], dim=-1)

            # Выбираем токен с наибольшей вероятностью
            _, predicted_token = torch.max(predicted_token_probs, dim=-1)
            # Пропускаем токен, если это препинание

            if id_to_word[predicted_token.item()] in [',', '.', '!', '?']:
                continue

            # Добавляем предсказанный токен к выводу
            tgt = torch.cat((tgt, predicted_token.unsqueeze(0)), dim=0)

            # Завершаем генерацию, если предсказан конец последовательности
            if predicted_token == word_to_id['<end>']:
                break

    # Преобразуем тензор с предсказанными индексами в текстовый формат
    print(tgt.T.squeeze().tolist())
    output_sentence = [id_to_word[idx] for idx in tgt.T.squeeze().tolist()]  # Fix the error here
    return " ".join(output_sentence)




def correcctor_txt(txt):
    return generate_sentence(model, txt.split(), word_to_id, id_to_word)
