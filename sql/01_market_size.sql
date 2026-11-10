SELECT
    month,
    ROUND(uk_ggy_cad_m, 1)                                                                    AS uk_ggy_cad_m,
    ROUND(uk_ggy_cad_m_grossed, 1)                                                            AS uk_ggy_cad_m_whole_market_est,
    ROUND(on_naggr_cad_m, 1)                                                                  AS on_naggr_cad_m,
    ROUND(100.0 * on_naggr_cad_m / NULLIF(uk_ggy_cad_m_grossed, 0), 1)                        AS on_share_of_uk_pct,
    ROUND(uk_ggy_cad_m_grossed / 53.9, 2)                                                     AS uk_ggy_cad_per_adult,
    ROUND(on_naggr_cad_m / 12.6, 2)                                                           AS on_naggr_cad_per_adult
FROM v_compare
WHERE month >= '2022-04'
ORDER BY month;

WITH yearly AS (
    SELECT
        SUBSTR(month, 1, 4) AS year,
        SUM(uk_ggy_cad_m)   AS uk_ggy_cad_m,
        SUM(on_naggr_cad_m) AS on_naggr_cad_m,
        COUNT(*)            AS months
    FROM v_compare
    WHERE month >= '2022-04' AND on_naggr_cad_m IS NOT NULL
    GROUP BY 1
)
SELECT
    year,
    months,
    ROUND(uk_ggy_cad_m, 0)                                                                      AS uk_ggy_cad_m,
    ROUND(on_naggr_cad_m, 0)                                                                    AS on_naggr_cad_m,
    ROUND(100.0 * (uk_ggy_cad_m / LAG(uk_ggy_cad_m) OVER (ORDER BY year) - 1), 1)               AS uk_yoy_pct,
    ROUND(100.0 * (on_naggr_cad_m / LAG(on_naggr_cad_m) OVER (ORDER BY year) - 1), 1)           AS on_yoy_pct
FROM yearly
ORDER BY year;

SELECT
    month,
    ROUND(on_naggr_cad_m, 1)                                                                     AS on_naggr_cad_m,
    ROUND(SUM(on_naggr_cad_m) OVER (ORDER BY month ROWS BETWEEN 11 PRECEDING AND CURRENT ROW), 0) AS on_naggr_trailing_12m,
    ROUND(100.0 * (on_naggr_cad_m / LAG(on_naggr_cad_m, 12) OVER (ORDER BY month) - 1), 1)       AS on_yoy_pct,
    ROUND(uk_ggy_cad_m, 1)                                                                       AS uk_ggy_cad_m,
    ROUND(100.0 * (uk_ggy_cad_m / LAG(uk_ggy_cad_m, 12) OVER (ORDER BY month) - 1), 1)           AS uk_yoy_pct
FROM v_compare
WHERE month >= '2022-04'
ORDER BY month;
