--
-- PostgreSQL database dump
--

-- Dumped from database version 11.5
-- Dumped by pg_dump version 11.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: nehapullabhotla
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO nehapullabhotla;

--
-- Name: product; Type: TABLE; Schema: public; Owner: nehapullabhotla
--

CREATE TABLE public.product (
    id integer NOT NULL,
    name character varying NOT NULL,
    date_purchased date,
    warranty_end_date date,
    user_id integer
);


ALTER TABLE public.product OWNER TO nehapullabhotla;

--
-- Name: product_id_seq; Type: SEQUENCE; Schema: public; Owner: nehapullabhotla
--

CREATE SEQUENCE public.product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_id_seq OWNER TO nehapullabhotla;

--
-- Name: product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nehapullabhotla
--

ALTER SEQUENCE public.product_id_seq OWNED BY public.product.id;


--
-- Name: sell_items; Type: TABLE; Schema: public; Owner: nehapullabhotla
--

CREATE TABLE public.sell_items (
    id integer NOT NULL,
    name character varying NOT NULL,
    warranty_period integer,
    item_description character varying,
    image_link character varying,
    user_id integer
);


ALTER TABLE public.sell_items OWNER TO nehapullabhotla;

--
-- Name: sell_items_id_seq; Type: SEQUENCE; Schema: public; Owner: nehapullabhotla
--

CREATE SEQUENCE public.sell_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sell_items_id_seq OWNER TO nehapullabhotla;

--
-- Name: sell_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nehapullabhotla
--

ALTER SEQUENCE public.sell_items_id_seq OWNED BY public.sell_items.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: nehapullabhotla
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying NOT NULL,
    email character varying NOT NULL
);


ALTER TABLE public.users OWNER TO nehapullabhotla;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: nehapullabhotla
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO nehapullabhotla;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nehapullabhotla
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: product id; Type: DEFAULT; Schema: public; Owner: nehapullabhotla
--

ALTER TABLE ONLY public.product ALTER COLUMN id SET DEFAULT nextval('public.product_id_seq'::regclass);


--
-- Name: sell_items id; Type: DEFAULT; Schema: public; Owner: nehapullabhotla
--

ALTER TABLE ONLY public.sell_items ALTER COLUMN id SET DEFAULT nextval('public.sell_items_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: nehapullabhotla
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: nehapullabhotla
--

COPY public.alembic_version (version_num) FROM stdin;
b9dc7c440935
\.


--
-- Data for Name: product; Type: TABLE DATA; Schema: public; Owner: nehapullabhotla
--

COPY public.product (id, name, date_purchased, warranty_end_date, user_id) FROM stdin;
1	Bluetooth	2018-05-12	2023-05-12	1
2	Iphone	2019-02-09	2025-02-09	2
4	MacBook	2017-01-12	2020-12-03	2
3	MacBook Pro	2017-01-12	2020-12-03	2
5	Macbook Pro	2017-01-12	2025-01-12	6
6	Macbook Pro	2017-01-12	2025-01-12	6
7	Macbook Pro	2017-01-12	2025-01-12	6
8	Macbook Pro	2017-01-12	2025-01-12	6
9	Macbook Pro	2017-01-12	2025-01-12	6
10	Macbook Pro	2017-01-12	2025-01-12	6
11	Macbook Pro	2017-01-12	2025-01-12	6
12	Macbook Pro	2017-01-12	2025-01-12	6
13	Macbook Pro	2017-01-12	2025-01-12	6
14	Macbook Pro	2017-01-12	2025-01-12	6
15	Macbook Pro	2017-01-12	2025-01-12	6
16	Macbook Pro	2017-01-12	2025-01-12	6
17	Macbook Pro	2017-01-12	2025-01-12	6
\.


--
-- Data for Name: sell_items; Type: TABLE DATA; Schema: public; Owner: nehapullabhotla
--

COPY public.sell_items (id, name, warranty_period, item_description, image_link, user_id) FROM stdin;
2	AirPods	2	Brand new and good quality	https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.macrumors.com%2Froundup%2Fairpods%2F&psig=AOvVaw3FxhZ76dz-ojBEsQk8uOQG&ust=1586242756694000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCPDjnfKc0-gCFQAAAAAdAAAAABAJ	2
3	Airpods	2	Brand new	blahblah	2
4	Airpods	2	Brand new	blahblah	5
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: nehapullabhotla
--

COPY public.users (id, name, email) FROM stdin;
1	Neha	nehapull@yahoo.com
2	lala	lala@yahoo.com
5	sakura@gmail.com	sakura@gmail.com
6	nehapullrox@gmail.com	nehapullrox@gmail.com
\.


--
-- Name: product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nehapullabhotla
--

SELECT pg_catalog.setval('public.product_id_seq', 17, true);


--
-- Name: sell_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nehapullabhotla
--

SELECT pg_catalog.setval('public.sell_items_id_seq', 4, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nehapullabhotla
--

SELECT pg_catalog.setval('public.users_id_seq', 6, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: nehapullabhotla
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: product product_pkey; Type: CONSTRAINT; Schema: public; Owner: nehapullabhotla
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);


--
-- Name: sell_items sell_items_pkey; Type: CONSTRAINT; Schema: public; Owner: nehapullabhotla
--

ALTER TABLE ONLY public.sell_items
    ADD CONSTRAINT sell_items_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: nehapullabhotla
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: product product_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nehapullabhotla
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: sell_items sell_items_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nehapullabhotla
--

ALTER TABLE ONLY public.sell_items
    ADD CONSTRAINT sell_items_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

