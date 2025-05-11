DROP PROCEDURE IF EXISTS insertar_json_array_data;
CREATE OR REPLACE PROCEDURE insertar_json_array_data(data JSONB)
LANGUAGE plpgsql
AS $$

BEGIN
    INSERT INTO charges (id, company_id, amount, status, created_at)
    SELECT 
        elem->>'id',
        elem->>'company_id',
        (elem->>'amount')::numeric,
        elem->>'status',
        (elem->>'created_at')::timestamp
    FROM jsonb_array_elements(data) AS elem
    ON CONFLICT (id) DO NOTHING;
END;
$$;
