import os
import pandas as pd


def analyze_sla_performance(
    file_path="data/processed/cleaned_complaints.csv",
):
    """Performs deep-dive SLA breach and operational bottleneck analysis."""
    if not os.path.exists(file_path):
        print(
            f"❌ Processed file missing at {file_path}. Run Milestone 4 first!"
        )
        return

    df = pd.read_csv(file_path)

    # Filter to resolved complaints for accurate SLA metrics
    resolved_df = df[df["is_resolved"] == 1].copy()

    total_resolved = len(resolved_df)
    total_breaches = int(resolved_df["is_sla_breached"].sum())
    overall_breach_rate = (total_breaches / total_resolved) * 100

    print("\n==================================================")
    print("      🚨 SLA PERFORMANCE & BOTTLENECK REPORT      ")
    print("==================================================")
    print(f"Total Resolved Complaints Audited : {total_resolved:,}")
    print(f"Total SLA Breaches                : {total_breaches:,}")
    print(f"Overall SLA Breach Rate           : {overall_breach_rate:.2f}%")

    # 1. Breach Analysis by Complaint Category
    print("\n--- 🔴 WORST-PERFORMING COMPLAINT CATEGORIES (SLA BREACHES) ---")
    category_summary = (
        resolved_df.groupby("complaint_type")
        .agg(
            total_cases=("unique_key", "count"),
            sla_breaches=("is_sla_breached", "sum"),
            avg_resolution_hrs=("resolution_time_hours", "mean"),
            median_resolution_hrs=("resolution_time_hours", "median"),
        )
        .reset_index()
    )

    category_summary["breach_rate_%"] = (
        category_summary["sla_breaches"] / category_summary["total_cases"]
    ) * 100

    # Filter categories with at least 100 cases for statistical significance
    significant_categories = category_summary[
        category_summary["total_cases"] >= 100
    ].sort_values(by="breach_rate_%", ascending=False)

    print(
        significant_categories[
            [
                "complaint_type",
                "total_cases",
                "sla_breaches",
                "breach_rate_%",
                "median_resolution_hrs",
            ]
        ]
        .head(7)
        .to_string(index=False)
    )

    # 2. Breach Analysis by Borough
    print("\n--- 🏙️ BOROUGH SLA PERFORMANCE BREAKDOWN ---")
    borough_summary = (
        resolved_df.groupby("borough")
        .agg(
            total_cases=("unique_key", "count"),
            sla_breaches=("is_sla_breached", "sum"),
            avg_resolution_hrs=("resolution_time_hours", "mean"),
            median_resolution_hrs=("resolution_time_hours", "median"),
        )
        .reset_index()
    )

    borough_summary["breach_rate_%"] = (
        borough_summary["sla_breaches"] / borough_summary["total_cases"]
    ) * 100

    print(
        borough_summary.sort_values(by="breach_rate_%", ascending=False)
        .to_string(index=False)
    )

    # Save summary report table to processed data
    summary_out = "data/processed/sla_summary_by_category.csv"
    significant_categories.to_csv(summary_out, index=False)
    print(f"\n💾 Saved category SLA metrics summary to: {summary_out}")


if __name__ == "__main__":
    analyze_sla_performance()