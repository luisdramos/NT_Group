CREATE VIEW amount_4_day AS
SELECT
    c.id AS company_id,
    c.name AS company_name,
    DATE(ch.created_at) AS fecha,
    SUM(ch.amount) AS monto_total
FROM charges ch
JOIN companies c ON ch.company_id = c.id
GROUP BY c.id, c.name, DATE(ch.created_at);
