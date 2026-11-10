WITH hold AS (
    SELECT
        month,
        product,
        cash_wagers_cad_m,
        naggr_cad_m,
        100.0 * naggr_cad_m / cash_wagers_cad_m AS hold_pct
    FROM on_product_monthly
    WHERE product IN ('betting', 'casino')
)
SELECT
    product,
    ROUND(AVG(hold_pct), 2)                                                   AS avg_hold_pct,
    ROUND(MIN(hold_pct), 2)                                                   AS min_hold_pct,
    ROUND(MAX(hold_pct), 2)                                                   AS max_hold_pct,
    ROUND(SQRT(AVG(hold_pct * hold_pct) - AVG(hold_pct) * AVG(hold_pct)), 2)  AS hold_sd_pp,
    ROUND(AVG(cash_wagers_cad_m), 0)                                          AS avg_wagers_cad_m,
    COUNT(*)                                                                  AS months
FROM hold
GROUP BY product;

WITH betting AS (
    SELECT
        month,
        cash_wagers_cad_m,
        naggr_cad_m,
        100.0 * naggr_cad_m / cash_wagers_cad_m AS hold_pct
    FROM on_product_monthly
    WHERE product = 'betting'
),
expected AS (
    SELECT
        month,
        cash_wagers_cad_m,
        naggr_cad_m,
        hold_pct,
        AVG(hold_pct) OVER (ORDER BY month ROWS BETWEEN 12 PRECEDING AND 1 PRECEDING) AS trailing_hold_pct,
        COUNT(*)      OVER (ORDER BY month ROWS BETWEEN 12 PRECEDING AND 1 PRECEDING) AS trailing_months
    FROM betting
)
SELECT
    month,
    cash_wagers_cad_m,
    naggr_cad_m,
    ROUND(hold_pct, 2)                                                  AS hold_pct,
    ROUND(trailing_hold_pct, 2)                                         AS trailing_hold_pct,
    ROUND(cash_wagers_cad_m * trailing_hold_pct / 100, 1)               AS expected_naggr_cad_m,
    ROUND(naggr_cad_m - cash_wagers_cad_m * trailing_hold_pct / 100, 1) AS result_effect_cad_m
FROM expected
WHERE trailing_months = 12
ORDER BY month;

WITH betting AS (
    SELECT
        SUBSTR(month, 1, 4) AS year,
        cash_wagers_cad_m,
        naggr_cad_m
    FROM on_product_monthly
    WHERE product = 'betting'
)
SELECT
    year,
    ROUND(100.0 * SUM(naggr_cad_m) / SUM(cash_wagers_cad_m), 2) AS hold_pct,
    ROUND(SUM(cash_wagers_cad_m), 0)                            AS wagers_cad_m,
    ROUND(SUM(naggr_cad_m), 1)                                  AS naggr_cad_m,
    COUNT(*)                                                    AS months
FROM betting
GROUP BY year
ORDER BY year;
