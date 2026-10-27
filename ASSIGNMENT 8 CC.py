import os
import re

os.environ.setdefault("KERAS_BACKEND", "torch")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
import keras
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
from keras._tf_keras.keras.preprocessing.text import Tokenizer

for pkg in ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4", "averaged_perceptron_tagger_eng"]:
    nltk.download(pkg, quiet=True)

pd.set_option("display.width", 250)
STOP = set(stopwords.words("english"))
WN = {"J": wordnet.ADJ, "V": wordnet.VERB, "R": wordnet.ADV}
ps, wl = PorterStemmer(), WordNetLemmatizer()
BLUE, SURFACE = "#2a78d6", "#fcfcfb"

# Q1

PARA = ("Formula One is my favourite sport because it blends raw speed with precise engineering. "
        "Every race weekend, ten teams push their cars to the limit on legendary circuits like Monza, Silverstone "
        "and Suzuka. I love watching the strategy unfold, especially when a well-timed pit stop changes the whole "
        "race! Drivers don't just need fast reflexes; they must also manage tyres, fuel and pressure for nearly two "
        "hours. The title fight between Hamilton and Verstappen was the most thrilling season I've ever watched. "
        "Even after the chequered flag, I keep analysing lap times and dreaming of watching a race live.")

clean = " ".join(re.sub(r"[^\w\s]", " ", PARA.lower()).split())
print("Q1.1 Lowercase text without punctuation:")
print(clean)

sents, words = sent_tokenize(PARA), word_tokenize(clean)
print(f"\nQ1.2 Sentence tokens ({len(sents)}):")
for s in sents:
    print(" -", s)
print(f"Word tokens ({len(words)}): {words}")

sp, wt = PARA.split(), word_tokenize(PARA)
print(f"\nQ1.3 split() ({len(sp)} tokens): {sp}")
print(f"word_tokenize() ({len(wt)} tokens): {wt}")
print(f"Only in split()        : {sorted(set(sp) - set(wt))}")
print(f"Only in word_tokenize(): {sorted(set(wt) - set(sp))}")
print("split() breaks only on whitespace, so punctuation stays attached to words ('engineering.', 'Monza,',")
print("'reflexes;') and the contraction 'don't' stays whole. word_tokenize() applies Penn Treebank rules: punctuation")
print("becomes separate tokens and 'don't' becomes 'do' + \"n't\", so it returns more tokens that are cleaner to count.")

filtered = [w for w in words if w not in STOP]
print(f"\nQ1.4 Tokens after stopword removal ({len(filtered)}): {filtered}")

fd = nltk.FreqDist(filtered)
print("\nQ1.5 Word frequency distribution (excluding stopwords):")
print(pd.DataFrame(fd.most_common(), columns=["Word", "Frequency"]).to_string(index=False))

top = fd.most_common(10)[::-1]
fig1, ax = plt.subplots(figsize=(7, 4.5), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
ax.barh([w for w, _ in top], [c for _, c in top], color=BLUE, height=0.6)
ax.set(title="Q1 Top 10 words (excluding stopwords)", xlabel="Frequency")
ax.xaxis.get_major_locator().set_params(integer=True)
ax.grid(axis="x", color="#e4e4e1", lw=0.8)
ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)
fig1.tight_layout()
fig1.savefig("A8_word_frequency.png", dpi=150)

# Q2

alpha = re.findall(r"(?<![\w'])[A-Za-z]+(?![\w'])", PARA)
print(f"\nQ2.1 Alphabetic words ({len(alpha)}): {alpha}")

q2 = [(w.lower(), t) for w, t in nltk.pos_tag(alpha) if w.lower() not in STOP]
print(f"\nQ2.2 After stopword removal ({len(q2)}): {[w for w, _ in q2]}")

q2 = pd.DataFrame([(w, t, ps.stem(w), wl.lemmatize(w, WN.get(t[0], wordnet.NOUN))) for w, t in q2],
                  columns=["Word", "POS", "Porter_Stem", "WordNet_Lemma"]).drop_duplicates()
print(f"\nQ2.3 Porter stems: {q2.Porter_Stem.tolist()}")
print(f"\nQ2.4 WordNet lemmas: {q2.WordNet_Lemma.tolist()}")

d = q2[q2.Porter_Stem != q2.WordNet_Lemma]
print(f"\nQ2.5 Words where stem and lemma differ ({len(d)} of {len(q2)}):")
print(d.to_string(index=False))
print("Stemming chops suffixes by rule, so it is fast but often produces non-words (engineering -> engin,")
print("precise -> precis, pressure -> pressur). Lemmatization looks words up in WordNet using the POS tag, so it")
print("returns real dictionary forms (changes -> change, not chang; analysing -> analyse, not analys) at a higher")
print("cost, but it depends on the tagger: 'dreaming' was tagged NN, so it was left unchanged.")
print("Prefer stemming for search engines, indexing and large-scale text classification, where speed and recall")
print("matter more than readable output. Prefer lemmatization for chatbots, question answering, sentiment analysis")
print("or any output a human reads, where the base word must stay meaningful.")

# Q3

DOCS = ["This phone has a brilliant camera and a brilliant display; the camera shines at night and the display "
        "stays sharp in sunlight. The battery lasts a full day.",
        "The battery drains quickly while gaming, the phone heats up during gaming, and the battery needs "
        "charging twice a day.",
        "The delivery was late, the phone arrived with a cracked screen, and the replacement delivery also came "
        "with a cracked screen."]
IDX = ["Text1", "Text2", "Text3"]

cv = CountVectorizer(stop_words="english")
bow = pd.DataFrame(cv.fit_transform(DOCS).toarray(), index=IDX, columns=cv.get_feature_names_out())
print("\nQ3.1 Bag of Words (CountVectorizer):")
print(bow.T.to_string())

tv = TfidfVectorizer(stop_words="english")
tfidf = pd.DataFrame(tv.fit_transform(DOCS).toarray(), index=IDX, columns=tv.get_feature_names_out())
print("\nQ3.2 TF-IDF scores (TfidfVectorizer):")
print(tfidf.T.round(3).to_string())

print("\nQ3.3 Top 3 TF-IDF keywords:")
for i, row in tfidf.iterrows():
    top3 = sorted(row.items(), key=lambda x: (-x[1], x[0]))[:3]
    print(f"{i}: " + ", ".join(f"{w} ({s:.3f}, in {(bow[w] > 0).sum()}/3 texts)" for w, s in top3))
print("Text1 is a positive review about the camera and display: 'brilliant', 'camera' and 'display' each occur")
print("twice and only in this text, so they get the highest weight. Text2 is a battery complaint: 'gaming' is")
print("repeated and unique, and 'battery' still ranks because it occurs twice even though Text1 also uses it;")
print("'charging' ties with the other one-off words of Text2 (drains, heats, needs, quickly, twice).")
print("Text3 is about delivery problems: 'cracked', 'delivery' and 'screen' are repeated and unique to it.")
print("'phone' appears in all three texts, so its IDF is minimal and it never becomes a keyword.")

# Q4

AI = """Artificial intelligence enables machines to learn patterns from large amounts of data.
Machine learning models improve their predictions as they process more data.
AI systems power voice assistants, recommendation engines and medical image analysis.
Training these models requires powerful hardware and carefully labelled data.
However, AI decisions can be hard to explain and may reflect hidden bias in the data."""
BC = """Blockchain is a distributed ledger that records transactions across many computers.
Each block stores a cryptographic hash of the previous block, forming a secure chain.
Because the data is shared and verified by consensus, records cannot be secretly changed.
Blockchain powers cryptocurrencies, smart contracts and supply chain tracking.
However, public blockchains can be slow and consume large amounts of energy."""


def preprocess(text):
    return [wl.lemmatize(w) for w in word_tokenize(re.sub(r"[^\w\s]", " ", text.lower())) if w not in STOP]


ta, tb = preprocess(AI), preprocess(BC)
print(f"\nQ4.1 AI tokens ({len(ta)}): {ta}")
print(f"Blockchain tokens ({len(tb)}): {tb}")

A, B = set(ta), set(tb)
jac = len(A & B) / len(A | B)
tv4 = TfidfVectorizer()
M = tv4.fit_transform([" ".join(ta), " ".join(tb)])
cos = cosine_similarity(M)[0, 1]
share = dict(zip(tv4.get_feature_names_out(), M[0].multiply(M[1]).toarray()[0] / cos))
print(f"\nQ4.2(a) Jaccard similarity = |A & B| / |A | B| = {len(A & B)}/{len(A | B)} = {jac:.4f}")
print(f"Shared tokens: {sorted(A & B)}")
print(f"Q4.2(b) Cosine similarity (TF-IDF) = {cos:.4f}")
print(f"\nQ4.2(c) Both scores are low, correctly showing that the texts describe different technologies. Jaccard only")
print(f"counts which words are shared ({len(A & B)} of {len(A | B)} unique words), so a one-off word such as 'however'")
print(f"counts as much as 'data'. Cosine with TF-IDF also uses frequency: 'data' occurs {ta.count('data')} times in the")
print(f"AI text, so it supplies {share['data']:.0%} of the cosine score while 'however' supplies only "
      f"{share['however']:.1%}, and the")
print("vectors are length-normalised so the longer text is not favoured. Cosine therefore gives the better insight here:")
print("it shows the main conceptual overlap is that both technologies depend on data.")

# Q5

REVIEWS = ["These earbuds sound amazing and the noise cancellation is excellent. Totally worth the price!",
           "Battery life is terrible and the left earbud keeps disconnecting. Very disappointed.",
           "The earbuds arrived on Tuesday in a box with a charging cable.",
           "Comfortable fit, clear calls and a beautiful charging case. I love them.",
           "The companion app is confusing and customer support was rude and unhelpful.",
           "Great bass and quick pairing, although the case feels slightly cheap."]

q5 = pd.DataFrame([(r, *TextBlob(r).sentiment) for r in REVIEWS], columns=["Review", "Polarity", "Subjectivity"])
q5["Sentiment"] = np.select([q5.Polarity > 0.05, q5.Polarity < -0.05], ["Positive", "Negative"], "Neutral")
print("\nQ5.1-5.2 TextBlob sentiment of earbud reviews:")
print(q5.round(3).to_string())

wc = WordCloud(width=900, height=450, background_color=SURFACE, stopwords=STOPWORDS, random_state=42,
               color_func=lambda *a, **k: BLUE).generate(" ".join(q5.Review[q5.Sentiment == "Positive"]).lower())
wc.to_file("A8_positive_wordcloud.png")
fig2, ax = plt.subplots(figsize=(9, 4.5), facecolor=SURFACE)
ax.imshow(wc, interpolation="bilinear")
ax.set_title("Q5 Word cloud of positive reviews")
ax.axis("off")
fig2.tight_layout()
print("\nQ5.3 Word cloud of positive reviews saved to A8_positive_wordcloud.png")

# Q6

CORPUS = ("The monsoon arrives in India like a long awaited guest. Dark clouds gather over the hills and the first "
          "rain falls on the dry earth. Children run into the streets and dance in the rain while farmers smile at "
          "the green fields. The smell of wet soil fills the air and the rivers begin to flow again. Every evening "
          "the sky turns grey and thunder rolls across the valley. The monsoon brings water, life and hope to "
          "millions of people. When the rain stops, the world looks fresh, clean and full of colour.")

tok = Tokenizer()
tok.fit_on_texts([CORPUS])
V = len(tok.word_index) + 1
seqs = [ids[:i + 1] for ids in tok.texts_to_sequences(sent_tokenize(CORPUS)) for i in range(1, len(ids))]
L = max(map(len, seqs))
seqs = keras.utils.pad_sequences(seqs, maxlen=L)
X, y = seqs[:, :-1], seqs[:, -1]
print(f"\nQ6.1 Training words: {len(CORPUS.split())}, vocabulary size: {V - 1}")
print(f"Word index: {tok.word_index}")
print(f"\nQ6.2 Input sequences: {len(seqs)}, padded length: {L}")
print(f"First 3 sequences (padded):\n{seqs[:3]}")

keras.utils.set_random_seed(42)
model = keras.Sequential([keras.Input((L - 1,)), keras.layers.Embedding(V, 32), keras.layers.LSTM(100),
                          keras.layers.Dense(V, activation="softmax")])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.summary()

h = model.fit(X, y, epochs=300, verbose=0).history
print(f"\nQ6.3 Final training loss: {h['loss'][-1]:.4f}, accuracy: {h['accuracy'][-1]:.4f}")


def generate(seed, n=10):
    for _ in range(n):
        x = keras.utils.pad_sequences(tok.texts_to_sequences([seed]), maxlen=L - 1)
        seed += " " + tok.index_word[int(model.predict(x, verbose=0)[0, 1:].argmax()) + 1]
    return seed


print("Generated text:")
for s in ["the monsoon", "dark clouds", "the sky"]:
    print(f"[{s}] {generate(s)}")

plt.show()
