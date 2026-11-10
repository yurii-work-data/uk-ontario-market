CREATE OR REPLACE VIEW v_fx AS
SELECT month, rate AS gbp_cad
FROM fx_monthly
WHERE pair = 'GBPCAD';

CREATE OR REPLACE VIEW v_uk AS
SELECT
    month,
    SUM(CASE WHEN metric = 'ggy_gbp' THEN value END) / 1e6                                      AS ggy_total_gbp_m,
    SUM(CASE WHEN metric = 'ggy_gbp' AND series = 'slots' THEN value END) / 1e6                 AS ggy_slots_gbp_m,
    SUM(CASE WHEN metric = 'ggy_gbp' AND series = 'casino' THEN value END) / 1e6                AS ggy_casino_gbp_m,
    SUM(CASE WHEN metric = 'ggy_gbp' AND series LIKE 'betting%' THEN value END) / 1e6           AS ggy_betting_gbp_m,
    SUM(CASE WHEN metric = 'ggy_gbp' AND series = 'poker' THEN value END) / 1e6                 AS ggy_poker_gbp_m,
    SUM(CASE WHEN metric = 'active_players' AND series = 'slots' THEN value END)                AS actives_slots,
    SUM(CASE WHEN metric = 'active_players' AND series = 'casino' THEN value END)               AS actives_casino,
    SUM(CASE WHEN metric = 'active_players' AND series = 'betting_real_event' THEN value END)   AS actives_betting,
    SUM(CASE WHEN metric = 'active_players' AND series = 'poker' THEN value END)                AS actives_poker,
    SUM(CASE WHEN metric = 'bets' AND series = 'slots' THEN value END)                          AS spins_slots,
    SUM(CASE WHEN metric = 'bets' AND series = 'betting_real_event' THEN value END)             AS bets_real_event,
    SUM(CASE WHEN metric = 'slots_sessions' AND series = 'sessions_total' THEN value END)       AS slot_sessions,
    SUM(CASE WHEN metric = 'slots_sessions' AND series = 'sessions_over_1h' THEN value END)     AS slot_sessions_over_1h,
    SUM(CASE WHEN metric = 'slots_sessions' AND series = 'avg_session_minutes' THEN value END)  AS slot_avg_session_min
FROM uk_online_monthly
WHERE month >= '2020-03'
GROUP BY month;

CREATE OR REPLACE VIEW v_on AS
SELECT
    m.month,
    m.fiscal_quarter,
    m.cash_wagers_cad_m,
    m.naggr_cad_m,
    m.active_accounts_k,
    m.arppa_cad,
    c.cash_wagers_cad_m AS wagers_casino_cad_m,
    c.naggr_cad_m       AS naggr_casino_cad_m,
    b.cash_wagers_cad_m AS wagers_betting_cad_m,
    b.naggr_cad_m       AS naggr_betting_cad_m,
    p.cash_wagers_cad_m AS wagers_poker_cad_m,
    p.naggr_cad_m       AS naggr_poker_cad_m
FROM on_market_monthly m
LEFT JOIN on_product_monthly c ON c.month = m.month AND c.product = 'casino'
LEFT JOIN on_product_monthly b ON b.month = m.month AND b.product = 'betting'
LEFT JOIN on_product_monthly p ON p.month = m.month AND p.product = 'poker';

CREATE OR REPLACE VIEW v_compare AS
SELECT
    u.month,
    u.ggy_total_gbp_m,
    u.ggy_total_gbp_m * f.gbp_cad                       AS uk_ggy_cad_m,
    u.ggy_total_gbp_m * f.gbp_cad / 0.7                 AS uk_ggy_cad_m_grossed,
    o.naggr_cad_m                                       AS on_naggr_cad_m,
    u.ggy_slots_gbp_m + u.ggy_casino_gbp_m              AS uk_gaming_gbp_m,
    u.ggy_betting_gbp_m                                 AS uk_betting_gbp_m,
    o.naggr_casino_cad_m,
    o.naggr_betting_cad_m,
    f.gbp_cad
FROM v_uk u
JOIN v_fx f USING (month)
LEFT JOIN v_on o USING (month);
