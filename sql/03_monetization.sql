SELECT
    month,
    ROUND(ggy_slots_gbp_m * 1e6 / actives_slots, 2)        AS uk_slots_ggy_per_active_gbp,
    ROUND(ggy_casino_gbp_m * 1e6 / actives_casino, 2)      AS uk_casino_ggy_per_active_gbp,
    ROUND(ggy_betting_gbp_m * 1e6 / actives_betting, 2)    AS uk_betting_ggy_per_active_gbp,
    ROUND(ggy_poker_gbp_m * 1e6 / actives_poker, 2)        AS uk_poker_ggy_per_active_gbp,
    ROUND(ggy_slots_gbp_m * 1e6 / spins_slots * 100, 3)    AS uk_slots_ggy_per_100_spins_gbp,
    ROUND(spins_slots / actives_slots, 0)                  AS uk_spins_per_slots_active
FROM v_uk
WHERE month >= '2020-04'
ORDER BY month;

SELECT
    month,
    arppa_cad                                               AS on_arppa_cad,
    ROUND(naggr_cad_m * 1e6 / (active_accounts_k * 1e3), 2) AS on_naggr_per_account_cad,
    ROUND(cash_wagers_cad_m / active_accounts_k * 1e3, 0)   AS on_wagers_per_account_cad,
    active_accounts_k
FROM v_on
ORDER BY month;

WITH uk AS (
    SELECT
        u.month,
        u.ggy_slots_gbp_m * 1e6 / u.actives_slots * f.gbp_cad AS uk_slots_per_active_cad,
        (u.ggy_slots_gbp_m + u.ggy_casino_gbp_m) * 1e6 / (u.actives_slots + u.actives_casino) * f.gbp_cad AS uk_gaming_per_active_cad
    FROM v_uk u
    JOIN v_fx f USING (month)
)
SELECT
    o.month,
    o.arppa_cad                                  AS on_arppa_cad,
    ROUND(uk.uk_slots_per_active_cad, 0)         AS uk_slots_ggy_per_active_cad,
    ROUND(uk.uk_gaming_per_active_cad, 0)        AS uk_gaming_ggy_per_active_cad
FROM v_on o
JOIN uk USING (month)
ORDER BY o.month;
