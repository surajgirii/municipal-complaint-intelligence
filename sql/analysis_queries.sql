-- SQL Query 1: Borough Performance

    SELECT 
        borough,
        COUNT(*) AS total_complaints,
        SUM(is_resolved) AS resolved_complaints,
        ROUND(AVG(resolution_time_hours), 2) AS avg_resolution_hours,
        SUM(CASE WHEN is_sla_breached = 1 THEN 1 ELSE 0 END) AS sla_breaches
    FROM complaints
    GROUP BY borough
    ORDER BY total_complaints DESC;
    

-- SQL Query 2: Category Ranking via Window Functions

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
    