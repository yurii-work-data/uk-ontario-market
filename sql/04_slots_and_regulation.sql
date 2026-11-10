SELECT
    month,
    ROUND(ggy_slots_gbp_m, 1)                                          AS slots_ggy_gbp_m,
    actives_slots,
    ROUND(spins_slots / 1e9, 2)                                        AS spins_bn,
    ROUND(slot_sessions / 1e6, 1)                                      AS sessions_m,
    ROUND(100.0 * slot_sessions_over_1h / slot_sessions, 1)            AS sessions_over_1h_pct,
    ROUND(slot_avg_session_min, 1)                                     AS avg_session_min,
    ROUND(spins_slots / slot_sessions, 0)                              AS spins_per_session,
    ROUND(ggy_slots_gbp_m * 1e6 / slot_sessions, 2)                    AS ggy_per_session_gbp,
    ROUND(ggy_slots_gbp_m * 1e6 / spins_slots * 100, 2)                AS ggy_per_100_spins_gbp,
    CASE
        WHEN month < '2025-04' THEN 'before stake limits'
        WHEN month < '2025-06' THEN 'transition (Apr-May 2025)'
        ELSE 'after stake limits'
    END                                                                AS period
FROM v_uk
WHERE month >= '2020-04'
ORDER BY month;

WITH labelled AS (
    SELECT
        month,
        ggy_slots_gbp_m,
        actives_slots,
        spins_slots,
        slot_sessions,
        slot_sessions_over_1h,
        CASE WHEN month BETWEEN '2024-06' AND '2025-03' THEN 'before'
             WHEN month BETWEEN '2025-06' AND '2026-03' THEN 'after' END AS period
    FROM v_uk
)
SELECT
    period,
    COUNT(*)                                                           AS months,
    ROUND(AVG(ggy_slots_gbp_m), 1)                                     AS avg_slots_ggy_gbp_m,
    ROUND(AVG(actives_slots) / 1e6, 2)                                 AS avg_actives_m,
    ROUND(AVG(ggy_slots_gbp_m * 1e6 / actives_slots), 2)               AS avg_ggy_per_active_gbp,
    ROUND(AVG(spins_slots / actives_slots), 0)                         AS avg_spins_per_active,
    ROUND(AVG(ggy_slots_gbp_m * 1e6 / spins_slots * 100), 3)           AS avg_ggy_per_100_spins_gbp,
    ROUND(AVG(100.0 * slot_sessions_over_1h / slot_sessions), 2)       AS avg_sessions_over_1h_pct
FROM labelled
WHERE period IS NOT NULL
GROUP BY period
ORDER BY period DESC;
