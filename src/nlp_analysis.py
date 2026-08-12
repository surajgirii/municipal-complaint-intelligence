import os
import re
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer

# Set aesthetic plot style
sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.size": 10, "figure.autolayout": True})


def clean_text(text):
    """Cleans raw text by removing numbers, punctuation, and converting to

    lowercase.
    """
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", " ", text)  # Keep only letters and spaces
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra whitespace
    return text


def run_nlp_analysis(
    file_path="data/processed/cleaned_complaints.csv",
    output_dir="reports/figures",
):
    """Performs TF-IDF and N-Gram analysis on descriptors to extract root causes

    and dominant complaint themes.
    """
    if not os.path.exists(file_path):
        print(f"❌ Processed file missing at {file_path}. Run Milestone 4 first!")
        return

    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(file_path)

    print("🔤 Running Business-Focused NLP Analysis...")

    # Combine descriptor and resolution_description for text context
    df["clean_text"] = (
        df["descriptor"].fillna("")
        + " "
        + df["resolution_description"].fillna("")
    ).apply(clean_text)

    # Filter non-empty text rows
    valid_text_df = df[df["clean_text"].str.strip() != ""].copy()

    # Custom stop words list to remove generic city terminology
    custom_stop_words = [
        "the",
        "and",
        "to",
        "of",
        "in",
        "a",
        "for",
        "is",
        "on",
        "that",
        "by",
        "this",
        "with",
        "i",
        "you",
        "it",
        "not",
        "or",
        "be",
        "are",
        "from",
        "at",
        "as",
        "was",
        "has",
        "have",
        "been",
        "will",
        "an",
        "city",
        "department",
        "nyc",
        "new",
        "york",
        "location",
        "report",
        "reported",
        "complaint",
        "action",
        "taken",
        "information",
        "service",
    ]

    # Initialize TF-IDF Vectorizer (Bi-grams: pairs of words like 'loud music', 'no heat')
    tfidf = TfidfVectorizer(
        ngram_range=(2, 2),  # Extract 2-word phrases (bigrams)
        stop_words=custom_stop_words,
        max_features=20,
    )

    tfidf_matrix = tfidf.fit_transform(valid_text_df["clean_text"])
    feature_names = tfidf.get_feature_names_out()
    tfidf_scores = tfidf_matrix.sum(axis=0).A1

    # Create top bi-gram phrase DataFrame
    phrase_df = (
        pd.DataFrame({"phrase": feature_names, "tfidf_score": tfidf_scores})
        .sort_values(by="tfidf_score", ascending=False)
        .head(10)
    )

    # --- Plot: Top Key Phrases (NLP) ---
    plt.figure(figsize=(10, 5))
    sns.barplot(
        x=phrase_df["tfidf_score"],
        y=phrase_df["phrase"],
        hue=phrase_df["phrase"],
        palette="Purples_r",
        legend=False,
    )
    plt.title(
        "Top Key Phrases in Complaints (TF-IDF Bi-grams)",
        fontsize=14,
        fontweight="bold",
    )
    plt.xlabel("TF-IDF Score (Prominence)")
    plt.ylabel("Extracted Key Phrase")
    plt.savefig(f"{output_dir}/05_nlp_top_phrases.png")
    plt.close()

    print("  ✅ Saved: 05_nlp_top_phrases.png")
    print("\n--- 🔝 TOP EXTRACTED COMPLAINT PHRASES ---")
    for idx, row in phrase_df.head(5).iterrows():
        print(f"  • {row['phrase'].title()} (TF-IDF: {row['tfidf_score']:.1f})")


if __name__ == "__main__":
    run_nlp_analysis()