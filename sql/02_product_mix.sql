WITH uk AS (
    SELECT
        SUBSTR(month, 1, 4) AS year,
        SUM(ggy_slots_gbp_m)   AS slots,
        SUM(ggy_casino_gbp_m)  AS casino,
        SUM(ggy_betting_gbp_m) AS betting,
        SUM(ggy_poker_gbp_m)   AS poker,
        SUM(ggy_total_gbp_m)   AS total
    FROM v_uk
    WHERE month >= '2020-04'
    GROUP BY 1
)
SELECT
    'UK' AS market,
    year,
    ROUND(100.0 * slots / total, 1)   AS slots_pct,
    ROUND(100.0 * casino / total, 1)  AS casino_pct,
    ROUND(100.0 * betting / total, 1) AS betting_pct,
    ROUND(100.0 * poker / total, 1)   AS poker_pct,
    ROUND(total, 0)                   AS total_gbp_m
FROM uk
ORDER BY year;

WITH o AS (
    SELECT
        SUBSTR(month, 1, 4) AS year,
        SUM(naggr_casino_cad_m)  AS casino,
        SUM(naggr_betting_cad_m) AS betting,
        SUM(naggr_poker_cad_m)   AS poker,
        SUM(naggr_cad_m)         AS total,
        SUM(wagers_casino_cad_m) AS wagers_casino,
        SUM(wagers_betting_cad_m) AS wagers_betting
    FROM v_on
    GROUP BY 1
)
SELECT
    'Ontario' AS market,
    year,
    ROUND(100.0 * casino / total, 1)   AS casino_pct,
    ROUND(100.0 * betting / total, 1)  AS betting_pct,
    ROUND(100.0 * poker / total, 1)    AS poker_pct,
    ROUND(100.0 * casino / wagers_casino, 2)   AS casino_hold_pct,
    ROUND(100.0 * betting / wagers_betting, 2) AS betting_hold_pct,
    ROUND(total, 0)                    AS total_cad_m
FROM o
ORDER BY year;

SELECT
    month,
    ROUND(100.0 * naggr_betting_cad_m / naggr_cad_m, 1)        AS on_betting_share_pct,
    ROUND(100.0 * naggr_betting_cad_m / wagers_betting_cad_m, 2) AS on_betting_hold_pct,
    ROUND(100.0 * naggr_casino_cad_m / wagers_casino_cad_m, 2)   AS on_casino_hold_pct
FROM v_on
ORDER BY month;
