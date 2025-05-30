﻿--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: insertar_json_array_comapnies(jsonb); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.insertar_json_array_comapnies(IN data jsonb)
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


ALTER PROCEDURE public.insertar_json_array_comapnies(IN data jsonb) OWNER TO postgres;

--
-- Name: insertar_json_array_data(jsonb); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.insertar_json_array_data(IN data jsonb)
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


ALTER PROCEDURE public.insertar_json_array_data(IN data jsonb) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: charges; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.charges (
    id character varying(40) NOT NULL,
    company_id character varying(40),
    amount numeric NOT NULL,
    status character varying(30) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone
);


ALTER TABLE public.charges OWNER TO postgres;

--
-- Name: companies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companies (
    id character varying(40) NOT NULL,
    name character varying(130) NOT NULL
);


ALTER TABLE public.companies OWNER TO postgres;

--
-- Name: charges charges_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.charges
    ADD CONSTRAINT charges_pkey PRIMARY KEY (id);


--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);


--
-- Name: charges charges_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.charges
    ADD CONSTRAINT charges_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- PostgreSQL database dump complete
--

