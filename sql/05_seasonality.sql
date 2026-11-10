WITH uk AS (
    SELECT
        month,
        CAST(SUBSTR(month, 6, 2) AS int) AS month_of_year,
        ggy_betting_gbp_m,
        ggy_slots_gbp_m,
        AVG(ggy_betting_gbp_m) OVER (ORDER BY month ROWS BETWEEN 6 PRECEDING AND 5 FOLLOWING) AS betting_12m_avg,
        AVG(ggy_slots_gbp_m)   OVER (ORDER BY month ROWS BETWEEN 6 PRECEDING AND 5 FOLLOWING) AS slots_12m_avg
    FROM v_uk
    WHERE month >= '2021-04'
)
SELECT
    month_of_year,
    ROUND(AVG(ggy_betting_gbp_m / betting_12m_avg) * 100, 1) AS uk_betting_season_index,
    ROUND(AVG(ggy_slots_gbp_m / slots_12m_avg) * 100, 1)     AS uk_slots_season_index,
    COUNT(*)                                                 AS observations
FROM uk
WHERE month BETWEEN '2022-04' AND '2025-09'
GROUP BY month_of_year
ORDER BY month_of_year;

WITH o AS (
    SELECT
        month,
        CAST(SUBSTR(month, 6, 2) AS int) AS month_of_year,
        naggr_betting_cad_m,
        naggr_casino_cad_m,
        AVG(naggr_betting_cad_m) OVER (ORDER BY month ROWS BETWEEN 6 PRECEDING AND 5 FOLLOWING) AS betting_12m_avg,
        AVG(naggr_casino_cad_m)  OVER (ORDER BY month ROWS BETWEEN 6 PRECEDING AND 5 FOLLOWING) AS casino_12m_avg
    FROM v_on
)
SELECT
    month_of_year,
    ROUND(AVG(naggr_betting_cad_m / betting_12m_avg) * 100, 1) AS on_betting_season_index,
    ROUND(AVG(naggr_casino_cad_m / casino_12m_avg) * 100, 1)   AS on_casino_season_index,
    COUNT(*)                                                   AS observations
FROM o
WHERE month BETWEEN '2023-04' AND '2026-03'
GROUP BY month_of_year
ORDER BY month_of_year;

SELECT
    u.month,
    ROUND(u.ggy_betting_gbp_m, 1)                                  AS uk_betting_ggy_gbp_m,
    ROUND(u.ggy_betting_gbp_m * 1e6 / u.bets_real_event, 2)        AS uk_ggy_per_bet_gbp,
    ROUND(u.actives_betting / 1e6, 2)                              AS uk_betting_actives_m,
    o.naggr_betting_cad_m                                          AS on_betting_naggr_cad_m,
    ROUND(100.0 * o.naggr_betting_cad_m / o.wagers_betting_cad_m, 2) AS on_betting_hold_pct
FROM v_uk u
LEFT JOIN v_on o USING (month)
WHERE u.month >= '2020-04'
ORDER BY u.month;
