import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set clean aesthetic plot style
sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.size": 10, "figure.autolayout": True})


def run_eda(
    file_path="data/processed/cleaned_complaints.csv",
    output_dir="reports/figures",
):
    """Generates analytical charts for complaint distribution, borough volume,

    resolution time, and SLA breach concentration.
    """
    if not os.path.exists(file_path):
        print(
            f"❌ Processed file missing at {file_path}. Run Milestone 4 first!"
        )
        return

    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(file_path)

    print("📊 Generating Exploratory Data Analysis (EDA) Visualizations...")

    # --- Chart 1: Top 10 Complaint Types ---
    plt.figure(figsize=(10, 5))
    top_complaints = df["complaint_type"].value_counts().head(10)
    sns.barplot(
        x=top_complaints.values,
        y=top_complaints.index,
        hue=top_complaints.index,
        palette="Blues_r",
        legend=False,
    )
    plt.title("Top 10 Municipal Complaint Types", fontsize=14, fontweight="bold")
    plt.xlabel("Total Complaints Count")
    plt.ylabel("Complaint Type")
    plt.savefig(f"{output_dir}/01_top_10_complaint_types.png")
    plt.close()
    print("  ✅ Saved: 01_top_10_complaint_types.png")

    # --- Chart 2: Complaints Distribution by Borough ---
    plt.figure(figsize=(8, 4))
    borough_counts = df["borough"].value_counts()
    sns.barplot(
        x=borough_counts.index,
        y=borough_counts.values,
        hue=borough_counts.index,
        palette="viridis",
        legend=False,
    )
    plt.title(
        "Complaint Distribution by Borough", fontsize=14, fontweight="bold"
    )
    plt.xlabel("Borough")
    plt.ylabel("Total Complaints Count")
    plt.xticks(rotation=15)
    plt.savefig(f"{output_dir}/02_complaints_by_borough.png")
    plt.close()
    print("  ✅ Saved: 02_complaints_by_borough.png")

    # --- Chart 3: Median Resolution Time by Top Complaint Type ---
    resolved_df = df[df["is_resolved"] == 1].copy()
    top_categories = top_complaints.index
    filtered_resolved = resolved_df[
        resolved_df["complaint_type"].isin(top_categories)
    ]

    plt.figure(figsize=(10, 5))
    median_times = (
        filtered_resolved.groupby("complaint_type")["resolution_time_hours"]
        .median()
        .sort_values(ascending=False)
    )
    sns.barplot(
        x=median_times.values,
        y=median_times.index,
        hue=median_times.index,
        palette="Reds_r",
        legend=False,
    )
    plt.title(
        "Median Resolution Time (Hours) by Top Categories",
        fontsize=14,
        fontweight="bold",
    )
    plt.xlabel("Median Resolution Time (Hours)")
    plt.ylabel("Complaint Type")
    plt.savefig(f"{output_dir}/03_median_resolution_time.png")
    plt.close()
    print("  ✅ Saved: 03_median_resolution_time.png")

    # --- Chart 4: SLA Breach Count by Top Complaint Type ---
    breach_df = df[df["is_sla_breached"] == 1]
    top_breaches = breach_df["complaint_type"].value_counts().head(10)

    plt.figure(figsize=(10, 5))
    sns.barplot(
        x=top_breaches.values,
        y=top_breaches.index,
        hue=top_breaches.index,
        palette="Oranges_r",
        legend=False,
    )
    plt.title(
        "Top 10 SLA Breach Categories", fontsize=14, fontweight="bold"
    )
    plt.xlabel("Number of SLA Breaches")
    plt.ylabel("Complaint Type")
    plt.savefig(f"{output_dir}/04_sla_breaches_by_category.png")
    plt.close()
    print("  ✅ Saved: 04_sla_breaches_by_category.png")

    print(
        f"\n🎉 All EDA charts successfully saved in directory: '{output_dir}'"
    )


if __name__ == "__main__":
    run_eda()