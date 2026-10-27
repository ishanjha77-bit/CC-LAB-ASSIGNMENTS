import pandas as pd
import re

#Q1 (a)

roll_number = input("Enter your college roll number: ").strip()

last_two_digits = roll_number[-2:]

digit1 = int(last_two_digits[0])
digit2 = int(last_two_digits[1])

categories = ["billing", "account", "general"]

category1 = categories[digit1 % 3]
category2 = categories[digit2 % 3]

#Q1 (b)

fixed_entries = [
    {
        "question": "what is the annual fee",
        "answer": "The annual fee is Rs 500.",
        "keywords": "fee cost price charge",
        "category": "billing"
    },
    {
        "question": "how to reset password",
        "answer": "Go to Settings > Reset Password.",
        "keywords": "password reset login",
        "category": "account"
    },
    {
        "question": "what are your working hours",
        "answer": "We are open 9 AM to 5 PM.",
        "keywords": "hours timing open time",
        "category": "general"
    },
    {
        "question": "how can i pay the fee",
        "answer": "You can pay via UPI, card, or net banking.",
        "keywords": "pay payment upi fee",
        "category": "billing"
    }
]

#Q1 (c)

# Dictionary containing sample questions and answers
# for each possible category.

personalized_data = {
    "billing": {
        "question": "how can i check my payment status",
        "answer": "You can check your payment status from the billing section.",
        "keywords": "payment status billing transaction"
    },

    "account": {
        "question": "how can i update my registered mobile number",
        "answer": "You can update your registered mobile number from account settings.",
        "keywords": "mobile number update account"
    },

    "general": {
        "question": "where can i find general information",
        "answer": "You can find general information in the help section.",
        "keywords": "information help details general"
    }
}

personalized_entry1 = {
    "question": personalized_data[category1]["question"],
    "answer": personalized_data[category1]["answer"],
    "keywords": personalized_data[category1]["keywords"],
    "category": category1
}

personalized_entry2 = {
    "question": personalized_data[category2]["question"],
    "answer": personalized_data[category2]["answer"],
    "keywords": personalized_data[category2]["keywords"],
    "category": category2
}

all_entries = fixed_entries + [
    personalized_entry1,
    personalized_entry2
]

df = pd.DataFrame(all_entries)

print("\n================ Q1: FINAL KNOWLEDGE BASE ================\n")
print(df.to_string(index=False))

#Q2 (a)

def score_query(query, df):
    """
    Takes a query string and returns all matching FAQ entries
    ranked according to their confidence score.
    """

    # Convert the query into lowercase words
    query_words = set(re.findall(r'\b\w+\b', query.lower()))

    results = []

    # Check every FAQ entry
    for index, row in df.iterrows():

        # Combine question and keywords for matching
        question_words = set(
            re.findall(r'\b\w+\b', row["question"].lower())
        )

        keyword_words = set(
            re.findall(r'\b\w+\b', row["keywords"].lower())
        )

        # Combine both sets of words
        searchable_words = question_words.union(keyword_words)

        # Calculate number of matching words
        matching_words = query_words.intersection(searchable_words)

        score = len(matching_words)

        # Only include entries having at least one match
        if score > 0:
            results.append({
                "index": index,
                "question": row["question"],
                "answer": row["answer"],
                "category": row["category"],
                "confidence": score,
                "matched_words": ", ".join(sorted(matching_words))
            })

    # Sort results from highest confidence to lowest
    results.sort(key=lambda x: x["confidence"], reverse=True)

    return results

#Q2 (b)

query = input("\nEnter a query for Q2: ")

results = score_query(query, df)

print("\n================ Q2: QUERY RESULTS ================\n")

if results:
    for result in results:
        print("Question   :", result["question"])
        print("Answer     :", result["answer"])
        print("Category   :", result["category"])
        print("Confidence :", result["confidence"])
        print("Matched    :", result["matched_words"])
        print("-" * 60)
else:
    print("No matching FAQ entry found.")

#Q3 (a)

def same_category(category_name, df):
    """
    Returns all FAQ entries belonging to the
    specified category.
    """

    return df[df["category"].str.lower() == category_name.lower()]

#Q3 (b)

print("\n================ Q3: SAME CATEGORY ================\n")

# Use the category of the first personalized entry
selected_category = category1

category_result = same_category(selected_category, df)

print("Selected Category:", selected_category)
print()

print(category_result.to_string(index=False))

#Q4 (a)

print("\n================ Q4: ADD NEW KEYWORD ================\n")

# Display FAQ entries so that the user can choose one
print("Available FAQ entries:\n")

for index, row in df.iterrows():
    print(f"{index}: {row['question']}")

# Ask the user to select an entry
selected_index = int(
    input("\nEnter the index of the FAQ entry to update: ")
)

# Ask the user for a new keyword
new_keyword = input("Enter a new keyword: ").strip().lower()

# Add the new keyword to the existing keywords
if new_keyword:
    existing_keywords = df.loc[selected_index, "keywords"]

    # Avoid duplicate keywords
    existing_keyword_list = existing_keywords.split()

    if new_keyword not in existing_keyword_list:
        df.loc[selected_index, "keywords"] = (
            existing_keywords + " " + new_keyword
        )

        print("\nNew keyword successfully added.")

    else:
        print("\nKeyword already exists.")

# Display updated entry
print("\nUpdated FAQ entry:\n")
print(df.loc[[selected_index]].to_string(index=False))

#Q4 (b)

csv_filename = f"{roll_number}_faq_data.csv"

df.to_csv(csv_filename, index=False)

print("\nUpdated DataFrame saved successfully as:")
print(csv_filename)

#Q5

print("\n================ Q5: CATEGORY COUNTS ================\n")

category_counts = (
    df.groupby("category")
      .size()
      .reset_index(name="FAQ_Count")
)

print(category_counts.to_string(index=False))

#Q6 (a)

def score_query_with_ties(query, df):
    """
    Modified version of Q2 scoring function.

    If multiple FAQ entries have the same highest score,
    all of them are displayed instead of selecting only one.
    """

    # Convert query into lowercase words
    query_words = set(re.findall(r'\b\w+\b', query.lower()))

    results = []

    # Calculate score for every FAQ entry
    for index, row in df.iterrows():

        question_words = set(
            re.findall(r'\b\w+\b', row["question"].lower())
        )

        keyword_words = set(
            re.findall(r'\b\w+\b', row["keywords"].lower())
        )

        searchable_words = question_words.union(keyword_words)

        matching_words = query_words.intersection(searchable_words)

        score = len(matching_words)

        if score > 0:
            results.append({
                "index": index,
                "question": row["question"],
                "answer": row["answer"],
                "category": row["category"],
                "confidence": score,
                "matched_words": ", ".join(sorted(matching_words))
            })

    # If no results were found
    if not results:
        print("No matching entries found.")
        return []

    # Sort by confidence
    results.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    # Find the highest score
    highest_score = results[0]["confidence"]

    # Select ALL entries having the highest score
    highest_matches = [
        result
        for result in results
        if result["confidence"] == highest_score
    ]

    print("\nHighest Confidence Score:", highest_score)

    # Display every equally good match
    if len(highest_matches) > 1:

        print("\nTIE DETECTED!")
        print("Multiple FAQ entries have the same highest score.\n")

        for result in highest_matches:
            print("Question   :", result["question"])
            print("Answer     :", result["answer"])
            print("Category   :", result["category"])
            print("Confidence :", result["confidence"])
            print("Matched    :", result["matched_words"])
            print("-" * 60)

    else:

        print("\nUnique Best Match:")
        print("Question   :", highest_matches[0]["question"])
        print("Answer     :", highest_matches[0]["answer"])
        print("Category   :", highest_matches[0]["category"])
        print("Confidence :", highest_matches[0]["confidence"])
        print("Matched    :", highest_matches[0]["matched_words"])

    return results

#Q6 (b)

print("\n================ Q6: TIE DEMONSTRATION ================\n")

print("Test Query 1: 'fee'")
print("\nExpected: Tie between the two billing-related fee entries.\n")

score_query_with_ties("fee", df)

#Q6 (c)

print("\n\nTest Query 2: 'password'")
print("\nExpected: One unique best match.\n")

score_query_with_ties("password", df)