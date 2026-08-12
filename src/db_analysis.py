import os
import sqlite3
import pandas as pd


def setup_database_and_query(
    csv_path="data/processed/cleaned_complaints.csv",
    db_path="data/municipal_complaints.db",
):
    """Loads cleaned CSV into SQLite database and executes analytical SQL queries."""
    if not os.path.exists(csv_path):
        print(f"❌ File missing at {csv_path}. Run Milestone 4 first!")
        return

    print("🗄️ Setting up SQLite Database & Executing Analytical SQL Queries...")

    # Load data into DataFrame
    df = pd.read_csv(csv_path)

    # Establish SQLite connection
    conn = sqlite3.connect(db_path)

    # Save DataFrame as a database table named 'complaints'
    df.to_sql("complaints", conn, if_exists="replace", index=False)
    print(f"  ✅ Data loaded into SQLite table 'complaints' ({len(df):,} rows)")

    # --- SQL Query 1: Borough-wise Resolution Performance ---
    query1 = """
    SELECT 
        borough,
        COUNT(*) AS total_complaints,
        SUM(is_resolved) AS resolved_complaints,
        ROUND(AVG(resolution_time_hours), 2) AS avg_resolution_hours,
        SUM(CASE WHEN is_sla_breached = 1 THEN 1 ELSE 0 END) AS sla_breaches
    FROM complaints
    GROUP BY borough
    ORDER BY total_complaints DESC;
    """

    print("\n--- 📊 QUERY 1: BOROUGH PERFORMANCE SUMMARY ---")
    df_q1 = pd.read_sql_query(query1, conn)
    print(df_q1.to_string(index=False))

    # --- SQL Query 2: Ranking Categories by SLA Breach Rate (Window Function) ---
    query2 = """
    WITH category_stats AS (
        SELECT 
            complaint_type,
            COUNT(*) AS total_cases,
            SUM(CASE WHEN is_sla_breached = 1 THEN 1 ELSE 0 END) AS breach_cases,
            ROUND(AVG(resolution_time_hours), 2) AS avg_hours
        FROM complaints
        WHERE is_resolved = 1
        GROUP BY complaint_type
        HAVING COUNT(*) >= 100
    )
    SELECT 
        complaint_type,
        total_cases,
        breach_cases,
        ROUND((CAST(breach_cases AS FLOAT) / total_cases) * 100, 2) AS breach_rate_pct,
        RANK() OVER (ORDER BY (CAST(breach_cases AS FLOAT) / total_cases) DESC) AS breach_rank
    FROM category_stats
    LIMIT 10;
    """

    print(
        "\n--- 🏆 QUERY 2: TOP BREACH CATEGORIES (RANKED VIA WINDOW FUNCTION) ---"
    )
    df_q2 = pd.read_sql_query(query2, conn)
    print(df_q2.to_string(index=False))

    # Save queries to sql/analysis_queries.sql for documentation
    os.makedirs("sql", exist_ok=True)
    with open("sql/analysis_queries.sql", "w") as f:
        f.write("-- SQL Query 1: Borough Performance\n" + query1 + "\n\n")
        f.write(
            "-- SQL Query 2: Category Ranking via Window Functions\n" + query2
        )

    print("\n💾 Queries saved to 'sql/analysis_queries.sql'")
    conn.close()


if __name__ == "__main__":
    setup_database_and_query()