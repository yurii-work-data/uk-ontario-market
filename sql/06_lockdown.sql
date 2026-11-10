WITH monthly AS (
    SELECT
        month,
        SUM(CASE WHEN series = 'betting_real_event' THEN value END) / 1e6 AS real_event_gbp_m,
        SUM(CASE WHEN series IN ('betting_virtual', 'betting_esports') THEN value END) / 1e6 AS virtual_esports_gbp_m,
        SUM(CASE WHEN series = 'slots' THEN value END) / 1e6 AS slots_gbp_m,
        SUM(CASE WHEN series = 'casino' THEN value END) / 1e6 AS casino_gbp_m,
        SUM(CASE WHEN series = 'poker' THEN value END) / 1e6 AS poker_gbp_m,
        SUM(value) / 1e6 AS total_gbp_m
    FROM uk_online_monthly
    WHERE metric = 'ggy_gbp'
      AND month BETWEEN '2020-03' AND '2020-12'
    GROUP BY month
),
base AS (
    SELECT * FROM monthly WHERE month = '2020-03'
)
SELECT
    m.month,
    ROUND(m.total_gbp_m, 1)                                              AS total_gbp_m,
    ROUND(m.real_event_gbp_m, 1)                                         AS real_event_gbp_m,
    ROUND(m.virtual_esports_gbp_m, 1)                                    AS virtual_esports_gbp_m,
    ROUND(m.slots_gbp_m, 1)                                              AS slots_gbp_m,
    ROUND(m.casino_gbp_m, 1)                                             AS casino_gbp_m,
    ROUND(m.poker_gbp_m, 1)                                              AS poker_gbp_m,
    ROUND(100.0 * (m.total_gbp_m / b.total_gbp_m - 1), 1)                AS total_vs_march_pct,
    ROUND(100.0 * (m.real_event_gbp_m / b.real_event_gbp_m - 1), 1)      AS real_event_vs_march_pct,
    ROUND(b.real_event_gbp_m - m.real_event_gbp_m, 1)                    AS real_event_shortfall_gbp_m,
    ROUND((m.slots_gbp_m + m.casino_gbp_m + m.poker_gbp_m + m.virtual_esports_gbp_m)
        - (b.slots_gbp_m + b.casino_gbp_m + b.poker_gbp_m + b.virtual_esports_gbp_m), 1) AS other_products_gain_gbp_m
FROM monthly m
CROSS JOIN base b
ORDER BY m.month;

SELECT
    month,
    SUM(CASE WHEN series = 'betting_real_event' THEN value END) / 1e6 AS betting_actives_m,
    SUM(CASE WHEN series = 'casino' THEN value END) / 1e6             AS casino_actives_m,
    SUM(CASE WHEN series = 'poker' THEN value END) / 1e6              AS poker_actives_m,
    SUM(CASE WHEN series = 'slots' THEN value END) / 1e6              AS slots_actives_m
FROM uk_online_monthly
WHERE metric = 'active_players'
  AND month BETWEEN '2020-03' AND '2020-12'
GROUP BY month
ORDER BY month;
