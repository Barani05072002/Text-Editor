import pickle

tokenizer_path = "C:/Users/Vebbox/nltk_data/tokenizers/punkt/english.pickle"

# Load manually, bypassing restrictions
with open(tokenizer_path, "rb") as f:
    tokenizer = pickle.load(f)

# Test tokenizer
text = "Hello world! How are you?"
print(tokenizer.tokenize(text))
