DROP PROCEDURE IF EXISTS insertar_json_array_comapnies;
CREATE OR REPLACE PROCEDURE insertar_json_array_comapnies(data JSONB)
LANGUAGE plpgsql
AS $$

BEGIN
    INSERT INTO companies (id, name)
    SELECT 
        elem->>'company_id',
        elem->>'name'
    FROM jsonb_array_elements(data) AS elem
    ON CONFLICT (id) DO NOTHING;
END;
$$;
