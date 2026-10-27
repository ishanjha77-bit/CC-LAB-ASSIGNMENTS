import re
import random, hashlib
import string
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, LancasterStemmer, RegexpStemmer, WordNetLemmatizer

ROLL_NO = 1024160099
NAME = "Ishan Jha"

for pkg in ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4",
            "averaged_perceptron_tagger", "averaged_perceptron_tagger_eng"]:
    nltk.download(pkg, quiet=True)

pd.set_option("display.width", 250)
pd.set_option("display.max_colwidth", 120)


def generate_dataset(roll_no):
    """Return (DataFrame of tickets, focus ticket IDs, fingerprint) for a roll number. Do not modify."""
    rng = random.Random(int(roll_no))

    subjects = [("LMS", ["LMS", "lms"]), ("Wi-Fi", ["Wi-Fi", "WiFi", "wifi"]), ("VPN", ["VPN"]),
                ("email", ["email", "e-mail"]), ("password", ["password"]), ("portal", ["student portal"]),
                ("projector", ["projector"]), ("laptop", ["laptop"]), ("MATLAB", ["MATLAB", "Matlab"]),
                ("Python", ["Python"]), ("printer", ["printer"]), ("server", ["server"])]
    actions = ["is not working", "keeps disconnecting", "failed to open", "is running slowly",
               "crashes while opening", "stopped responding", "is showing an error", "was working yesterday",
               "has stopped syncing", "keeps asking for login"]
    user_actions = ["cannot access", "can't open", "couldn't connect to", "am unable to use",
                    "tried restarting", "was locked out of", "keep getting logged out of", "reinstalled"]
    contexts = ["after resetting my password", "during the lab", "on my laptop", "since yesterday",
                "after the latest update", "when I use mobile hotspot", "before the assignment deadline",
                "while uploading the file", "after restarting the system", "when connected to campus Wi-Fi"]
    endings = ["Please help.", "Can you check this?", "I have tried several times!", "It worked yesterday.",
               "I don't know what changed.", "The same problem occurs again.", "Is there another solution?",
               "It works on another computer.", "This is urgent.", "Please resolve it."]
    challenges = {
        "negation": ["The Wi-Fi works, but the VPN doesn't.", "Why isn't the portal opening?",
                     "I can't login and I didn't change anything.", "It's not the laptop; it's the server.",
                     "Nothing works and nobody has replied.", "The printer won't print; it isn't jammed."],
        "numbers": ["Python 3.12 was installed yesterday.", "The file is 95.5% uploaded.",
                    "Error code 0x80070005 appears.", "I need Windows 11 by 5.30 p.m. today.",
                    "Only 2 of 30 PCs boot after 3.5 hours.", "Version 2.0.1 crashes at 99%."],
        "identifiers": ["Email me at helpdesk@university.edu.", "See https://lms.thapar.edu/help for details.",
                        "My roll no. is 1023-03-021.", "Ticket #4521 is still open.",
                        "Call me on +91 98765 43210 or 0175-239-3201.",
                        "Write to it.helpdesk@thapar.edu or visit www.thapar.edu/it."],
        "punctuation": ["I tried again... still no response!!!", "The LMS says 'Not Submitted'.",
                        "Dr. Rao's lab PC (No. 14) is down.", "Is it fixed?? Pls reply ASAP :(",
                        "The state-of-the-art lab (Lab-3) is closed.", "Re-installing didn't help; log-in still fails!"],
    }

    tickets = []
    for _ in range(8 + int(roll_no) % 5):
        _, variants = rng.choice(subjects)
        s = rng.choice(variants)
        template = rng.randrange(3)
        if template == 0:
            text = f"{s} {rng.choice(actions)} {rng.choice(contexts)}. {rng.choice(endings)}"
        elif template == 1:
            text = f"I {rng.choice(user_actions)} the {s} {rng.choice(contexts)}. {rng.choice(endings)}"
        else:
            text = f"The {s} {rng.choice(actions)}. {rng.choice(endings)}"
        tickets.append(text[0].upper() + text[1:])
    for category in ["negation", "numbers", "identifiers", "punctuation"]:
        tickets.append(rng.choice(challenges[category]))
    rng.shuffle(tickets)

    df = pd.DataFrame({"Ticket_ID": [f"T{i + 1:02d}" for i in range(len(tickets))], "Ticket_Text": tickets})
    focus = [f"T{i:02d}" for i in sorted(rng.sample(range(1, len(tickets) + 1), 2))]
    fingerprint = hashlib.md5(("|".join(tickets) + str(int(roll_no))).encode()).hexdigest()[:8].upper()
    return df, focus, fingerprint


STOP = set(stopwords.words("english"))

def is_punct(token):
    """A token is punctuation if EVERY character in it is in string.punctuation (e.g. '.', '...', '``', "''")."""
    return all(ch in string.punctuation for ch in token)

def process_ticket(text):
    """The official pipeline. Returns sentences, lowercase tokens, punctuation, stopwords and final tokens."""
    sentences = sent_tokenize(text)
    tokens = [t.lower() for s in sentences for t in word_tokenize(s)]
    punct = [t for t in tokens if is_punct(t)]
    stops = [t for t in tokens if t in STOP]
    final = [t for t in tokens if not is_punct(t) and t not in STOP]
    return {"sentences": sentences, "tokens": tokens, "punct": punct, "stops": stops, "final": final}


df, FOCUS, FINGERPRINT = generate_dataset(ROLL_NO)
print(f"Roll number: {ROLL_NO}   Name: {NAME}   Fingerprint: {FINGERPRINT}   Tickets: {len(df)}\n")
print(df.to_string(index=False))
df.to_csv(f"{ROLL_NO}_generated_dataset.csv", index=False)
TEXT = dict(zip(df.Ticket_ID, df.Ticket_Text))

# Q1

res = {i: process_ticket(t) for i, t in TEXT.items()}
q1 = pd.DataFrame([{"Ticket_ID": i, "Sentences": len(r["sentences"]), "Tokens": len(r["tokens"]),
                    "Punctuation": len(r["punct"]), "Stopwords": len(r["stops"]),
                    "Unique_Tokens": len(set(r["tokens"])), "Final_Tokens": len(r["final"])}
                   for i, r in res.items()])
q1.loc[len(q1)] = ["TOTAL", *q1.iloc[:, 1:].sum()]

print("\nQ1 Preprocessing summary:")
print(q1.to_string(index=False))

sel = FOCUS[0]
print(f"\nQ1 Selected ticket {sel}: {TEXT[sel]}")
for k, lbl in [("tokens", "Tokens"), ("punct", "Punctuation tokens"), ("stops", "Stopwords"), ("final", "Final tokens")]:
    print(f"{lbl:<19}: {res[sel][k]}")

uniq = sorted({t for r in res.values() for t in r["final"]})
odd = [t for t in uniq if not re.fullmatch(r"[a-z]+(?:-[a-z]+)*", t)]
print(f"\nQ1 Observe: final tokens that are not plain words: {odd} (plus 'https')")
print("n't comes from word_tokenize splitting don't/didn't/doesn't: do/did/does are stopwords, but n't is neither a")
print("stopword nor pure punctuation, so it survives. 'https' and '//lms.thapar.edu/help' come from the T07 URL being")
print("split at ':'. 2, 30 and 3.5 are numbers from T15. 'cannot' is split into can + not and both are removed as stopwords.")

# Q2

TEST_LINES = [
    "Mail it.helpdesk@thapar.edu or a.b-c@dept.univ.ac.in; visit https://lms.thapar.edu/help or www.thapar.edu/it.",
    "Call +91 98765 43210, +91-98765-43210 or 0175-239-3201. Version 2.0.1 is 95.5% done; fee Rs 1,250.",
    "The state-of-the-art lab isn't open; log-in at 5.30 p.m. didn't work.",
]

L, R, W = r"(?<![\w@./:-])(?<![A-Za-z]')", r"(?![\w@/:]|[.'-][A-Za-z])", r"[A-Za-z]*(?:['-][A-Za-z]+)*"
FIND = {
    "Words > 5 letters": L + r"(?=(?:[A-Za-z]['-]?){6})[A-Za-z]" + W + R,
    "Numbers": r"(?<![\w.])(?:0[xX][0-9A-Fa-f]+|\d+(?:,\d{3}(?!\d))*(?:\.\d+)*)",
    "Capitalized words": L + r"[A-Z]" + W + R,
    "Vowel-initial words": L + r"[AEIOUaeiou]" + W + R,
}
EMAIL = r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"
URL = r"(?:https?://|www\.)\S+?(?=[.,;:!?)\"']*(?:\s|$))"
PHONE = r"(?<!\w)(?:\+\d{1,3}[\s-]?)?(?:\d{5}[\s-]?\d{5}|0\d{2,4}[\s-]\d{3,4}[\s-]\d{4})(?!\w)"


def mask(text):
    return re.sub(PHONE, "<PHONE>", re.sub(URL, "<URL>", re.sub(EMAIL, "<EMAIL>", text)))


print("\nQ2 re.findall on raw tickets:")
for k, p in FIND.items():
    m = [x for t in TEXT.values() for x in re.findall(p, t)]
    print(f"{k} ({len(m)}): {m}")

print("\nQ2 re.findall on TEST_LINES:")
for n, line in enumerate(TEST_LINES, 1):
    print(f"Line {n}:")
    for k, p in FIND.items():
        print(f"  {k}: {re.findall(p, line)}")

print("\nQ2 re.sub on TEST_LINES:")
for line in TEST_LINES:
    print(mask(line))
print("\nQ2 re.sub on raw tickets (changed tickets only):")
for i, t in TEXT.items():
    if mask(t) != t:
        print(f"{i}: {t}\n  -> {mask(t)}")

caps = [(t, m) for t in TEXT.values() for m in re.finditer(FIND["Capitalized words"], t)]
init = [m.group() for t, m in caps if re.fullmatch(r"(?:.*[.!?]\s+)?", t[:m.start()]) and m.group()[1:].islower()]
print(f"\nQ2 Observe: {len(init)} of {len(caps)} capitalized words are capitalized only because they start a sentence: "
      f"{dict(Counter(init))}")

# Q3

TOKENIZER = RegexpTokenizer("|".join([URL, EMAIL, PHONE, r"(?:[A-Za-z]\.){2,}", r"\d+(?:\.\d+)+",
                                      r"\d{1,3}(?:,\d{3})+", r"\w+(?:['-]\w+)*", r"\.{3}|[!?]+|[^\w\s]"]))


def my_tokenize(text):
    return TOKENIZER.tokenize(text)


print("\nQ3 my_tokenize on TEST_LINES:")
for line in TEST_LINES:
    print(my_tokenize(line))
print("\nQ3 my_tokenize on tickets:")
for i, t in TEXT.items():
    print(f"{i}: {my_tokenize(t)}")

q3 = []
for i, t in [*((f"TEST{n}", l) for n, l in enumerate(TEST_LINES, 1)), *TEXT.items()]:
    a, b = Counter(word_tokenize(t)), Counter(my_tokenize(t))
    if a != b:
        q3.append((i, list((a - b).elements()), list((b - a).elements())))
q3 = pd.DataFrame(q3, columns=["Text", "Only in word_tokenize", "Only in my_tokenize"])
print("\nQ3 Differences between word_tokenize() and my_tokenize():")
print(q3.to_string(index=False))
print("\nQ3 Explanation of differences:")
print("1. Contractions (T02 don't, T11 didn't, T12 doesn't, TEST3 isn't): word_tokenize follows Penn Treebank rules and")
print("   splits off the clitic (do + n't); my pattern \\w+(?:['-]\\w+)* keeps the apostrophe inside one token.")
print("2. 'cannot' (T04): the Treebank tokenizer has a special rule that splits it into can + not; my pattern treats it as")
print("   one run of word characters.")
print("3. URLs (T07, TEST1): word_tokenize breaks https://lms.thapar.edu/help at ':' into https, :, //lms.thapar.edu/help;")
print("   my URL alternative is tried first and consumes the whole address up to whitespace/trailing punctuation.")
print("4. Emails (TEST1): word_tokenize separates '@' (it.helpdesk, @, thapar.edu); my email alternative keeps it whole.")
print("5. Spaced phone numbers (TEST2): word_tokenize splits '+91 98765 43210' on whitespace; my phone alternative spans")
print("   the internal spaces and returns one token.")
print(f"\nQ3 Observe: {(~q3.Text.str.startswith('TEST')).sum()} of {len(df)} tickets are tokenized differently.")

# Q4

tags = {}
for t in TEXT.values():
    for w, p in nltk.pos_tag([w for s in sent_tokenize(t) for w in word_tokenize(s)]):
        tags.setdefault(w.lower(), p)
WN = {"J": wordnet.ADJ, "V": wordnet.VERB, "R": wordnet.ADV}
ps, ls, wl = PorterStemmer(), LancasterStemmer(), WordNetLemmatizer()
rs = RegexpStemmer("ing$", min=6)
ing = [w for w in uniq if w.endswith("ing")]
print(f"\nQ4 RegexpStemmer suffix 'ing$' (min=6): {len(ing)} unique final tokens end in -ing: {ing}")
print("-ing is the most frequent inflectional suffix in this dataset (e.g. running, showing, restarting), so stripping it")
print("groups the most verb forms; min=6 stops short words such as 'thing' or 'king' from being stemmed.")

q4 = pd.DataFrame([(w, tags[w], ps.stem(w), ls.stem(w), rs.stem(w), wl.lemmatize(w, WN.get(tags[w][0], wordnet.NOUN)))
                   for w in uniq], columns=["Word", "POS", "Porter", "Lancaster", "Regexp", "WordNet"])
q4 = q4[q4.iloc[:, 2:].nunique(axis=1) > 1]
print(f"\nQ4 Words where the outputs differ ({len(q4)} of {len(uniq)}):")
print(q4.to_string(index=False))
print(f"\nQ4 Observe: Over-stemming - Lancaster 'printer' -> '{ls.stem('printer')}' merges the device with the verb 'print'.")
print(f"Under-stemming - Porter 'reinstalled' -> '{ps.stem('reinstalled')}' but 're-installing' -> "
      f"'{ps.stem('re-installing')}', so two forms of the same verb get different stems.")

# Q5

S = {"S1": [t for r in res.values() for t in r["tokens"]]}
S["S2"] = [t for t in S["S1"] if not is_punct(t)]
S["S3"] = [t for r in res.values() for t in r["final"]]
S["S4"] = [ps.stem(t) for t in S["S3"]]
q5 = pd.DataFrame([(k, len(v), len(set(v)), round(len(set(v)) / len(v), 4)) for k, v in S.items()],
                  columns=["Set", "Total_Tokens", "Unique_Tokens", "TTR"])
print("\nQ5 Corpus statistics:")
print(q5.to_string(index=False))

for k in ("S1", "S3"):
    print(f"\nQ5 Top 10 words of {k}: {Counter(S[k]).most_common(10)}")

freq = sorted(Counter(S["S3"]).values(), reverse=True)
fig, ax = plt.subplots(figsize=(7, 4.5), facecolor="#fcfcfb")
ax.set_facecolor("#fcfcfb")
ax.plot(np.log(np.arange(1, len(freq) + 1)), np.log(freq), "-o", color="#2a78d6", lw=2, ms=6)
ax.set(title="S3 final tokens: log(rank) vs log(frequency)", xlabel="log(rank)", ylabel="log(frequency)")
ax.grid(color="#e4e4e1", lw=0.8)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(f"{ROLL_NO}_zipf_S3.png", dpi=150)

for k, key in (("S1", "tokens"), ("S3", "final")):
    bg = Counter(b for r in res.values() for b in nltk.bigrams(r[key]))
    print(f"\nQ5 Top 5 bigrams of {k}: {bg.most_common(5)}")

# Q6

T = q5.set_index("Set")
grp = {}
for w in uniq:
    grp.setdefault(ps.stem(w), []).append(w)
merged = [g for g in grp.values() if len(g) > 1]
wt, mt = word_tokenize(TEXT["T07"]), my_tokenize(TEXT["T07"])

print("\nQ6 Interpretation:")
print(f"(a) S1 (TTR {T.TTR.S1}) is dominated by repeated punctuation ('.' occurs {S['S1'].count('.')} times) and stopwords")
print(f"    (the, is, i). S2 removes {T.Total_Tokens.S1 - T.Total_Tokens.S2} punctuation tokens but only "
      f"{T.Unique_Tokens.S1 - T.Unique_Tokens.S2} types, so TTR rises to {T.TTR.S2}.")
print(f"    S3 removes {T.Total_Tokens.S2 - T.Total_Tokens.S3} stopword tokens (the most repeated words) but only "
      f"{T.Unique_Tokens.S2 - T.Unique_Tokens.S3} types, so TTR rises to {T.TTR.S3}.")
print(f"    S4 keeps all {T.Total_Tokens.S4} tokens but Porter merges {merged} into one stem, so types fall "
      f"{T.Unique_Tokens.S3} -> {T.Unique_Tokens.S4} and TTR drops slightly to {T.TTR.S4}.")
print(f"(b) T07 URL: word_tokenize gives {wt} because the Treebank rules split at ':'; my_tokenize gives {mt}")
print("    because its URL alternative matches the whole address before any punctuation rule is tried.")
print(f"(c) Porter stems 'several' -> '{ps.stem('several')}', which is a different English verb (to cut), so the "
      f"meaning changes; Lancaster 'unable' -> '{ls.stem('unable')}' loses the meaning entirely.")
print(f"(d) 'tried' (POS {tags['tried']}) is lemmatized as a verb to '{wl.lemmatize('tried', wordnet.VERB)}', a real "
      f"dictionary word, while Porter and Lancaster both give the non-word '{ps.stem('tried')}'.")

plt.show()
