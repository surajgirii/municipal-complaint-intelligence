import os
import numpy as np
import pandas as pd

# SLA Target Assumptions (in Hours) per major complaint category
# (Used when city does not publish explicit per-complaint SLA guidelines)
DEFAULT_SLA_MAPPING = {
    "HEAT/HOT WATER": 24,
    "PLUMBING": 48,
    "ILLEGAL PARKING": 12,
    "NOISE - RESIDENTIAL": 12,
    "BLOCKED DRIVEWAY": 24,
    "RODENT": 72,
    "UNSANITARY CONDITION": 48,
    "STREET LIGHT OUT": 72,
    "WATER SYSTEM": 48,
    "PAINT/PLASTER": 120,
}
DEFAULT_FALLBACK_SLA_HOURS = 48  # Default SLA for unmapped categories


def clean_and_feature_engineer(
    raw_path="data/raw/raw_complaints.csv",
    processed_path="data/processed/cleaned_complaints.csv",
):
    """Cleans raw complaint data, converts timestamps, calculates resolution

    times, and engineers SLA breach flags.
    """
    if not os.path.exists(raw_path):
        print(f"❌ Raw file not found at {raw_path}. Run Milestone 2 first!")
        return

    print("⏳ Reading raw data...")
    df = pd.read_csv(raw_path)
    initial_count = len(df)

    # 1. Standardize column names (strip spaces, lowercase)
    df.columns = df.columns.str.strip().str.lower()

    # 2. Parse Datetime columns
    print("⏳ Parsing datetime columns...")
    df["created_date"] = pd.to_datetime(
        df["created_date"], errors="coerce", utc=True
    )
    df["closed_date"] = pd.to_datetime(
        df["closed_date"], errors="coerce", utc=True
    )

    # Remove offset timezone for easier querying & export
    df["created_date"] = df["created_date"].dt.tz_localize(None)
    df["closed_date"] = df["closed_date"].dt.tz_localize(None)

    # 3. Filter invalid records (missing created_date or created after closed)
    df = df[df["created_date"].notnull()].copy()
    df = df[
        (df["closed_date"].isnull())
        | (df["closed_date"] >= df["created_date"])
    ].copy()

    # 4. Feature Engineering: Resolution Time
    df["is_resolved"] = df["closed_date"].notnull().astype(int)

    # Calculate resolution time in hours and days
    df["resolution_time_hours"] = np.where(
        df["is_resolved"] == 1,
        (df["closed_date"] - df["created_date"]).dt.total_seconds() / 3600.0,
        np.nan,
    )
    df["resolution_time_days"] = (df["resolution_time_hours"] / 24.0).round(2)
    df["resolution_time_hours"] = df["resolution_time_hours"].round(2)

    # 5. Feature Engineering: Date Attributes (for Time-Series analysis)
    df["created_year"] = df["created_date"].dt.year
    df["created_month"] = df["created_date"].dt.month
    df["created_month_name"] = df["created_date"].dt.strftime("%b")
    df["created_day_name"] = df["created_date"].dt.strftime("%a")
    df["created_hour"] = df["created_date"].dt.hour

    # 6. Feature Engineering: SLA Benchmarks & SLA Breach Flag
    df["sla_target_hours"] = (
        df["complaint_type"]
        .map(DEFAULT_SLA_MAPPING)
        .fillna(DEFAULT_FALLBACK_SLA_HOURS)
    )

    df["is_sla_breached"] = np.where(
        df["is_resolved"] == 1,
        (df["resolution_time_hours"] > df["sla_target_hours"]).astype(int),
        np.nan,  # SLA breach status pending for unresolved complaints
    )

    # 7. Clean location attributes
    df["borough"] = df["borough"].fillna("UNSPECIFIED").str.upper()
    df["city"] = df["city"].fillna("UNKNOWN").str.title()

    # Save processed data
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    df.to_csv(processed_path, index=False)

    print("\n✅ DATA CLEANING & FEATURE ENGINEERING COMPLETE")
    print(f"📊 Initial Rows: {initial_count:,}")
    print(f"📊 Processed Rows: {len(df):,}")
    print(
        f"⏱️ Resolved Complaints: {df['is_resolved'].sum():,} / {len(df):,}"
    )
    print(
        f"🚨 Total SLA Breaches: {int(df['is_sla_breached'].sum()):,} ({df['is_sla_breached'].mean()*100:.2f}%)"
    )
    print(f"📁 Processed file saved to: {processed_path}")


if __name__ == "__main__":
    clean_and_feature_engineer()