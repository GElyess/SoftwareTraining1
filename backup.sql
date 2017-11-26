--
-- PostgreSQL database dump
--

-- Dumped from database version 10.0
-- Dumped by pg_dump version 10.0

-- Started on 2017-11-12 08:14:49

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12924)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2874 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- TOC entry 224 (class 1255 OID 16853)
-- Name: comment_likes_add(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION comment_likes_add() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
update public.comments set likes = likes+1 where comment_id = NEW.comment_id;
return NEW;
end;
$$;


ALTER FUNCTION public.comment_likes_add() OWNER TO postgres;

--
-- TOC entry 228 (class 1255 OID 16854)
-- Name: comment_likes_minus(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION comment_likes_minus() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
update public.comments set likes = likes-1 where comment_id = OLD.comment_id;
return OLD;
end;
$$;


ALTER FUNCTION public.comment_likes_minus() OWNER TO postgres;

--
-- TOC entry 210 (class 1255 OID 16855)
-- Name: follow_add(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION follow_add() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
update public.user set follow_number = follow_number+1 where public.user.id = NEW.user_follow_id;
return NEW;
end;
$$;


ALTER FUNCTION public.follow_add() OWNER TO postgres;

--
-- TOC entry 212 (class 1255 OID 16856)
-- Name: follow_minus(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION follow_minus() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
update public.user set follow_number = follow_number-1 where public.user.id = OLD.user_follow_id;
return OLD;
end;
$$;


ALTER FUNCTION public.follow_minus() OWNER TO postgres;

--
-- TOC entry 220 (class 1255 OID 16857)
-- Name: follower_add(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION follower_add() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
update public.user set follower_number = follower_number+1 where id = NEW.user_followed_id;
return new;
end;
$$;


ALTER FUNCTION public.follower_add() OWNER TO postgres;

--
-- TOC entry 213 (class 1255 OID 16858)
-- Name: follower_minus(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION follower_minus() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
update public.user set follower_number = follower_number-1 where public.user.id = OLD.user_followed_id;
return OLD;
end;
$$;


ALTER FUNCTION public.follower_minus() OWNER TO postgres;

--
-- TOC entry 227 (class 1255 OID 16859)
-- Name: post_comments_number_add(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION post_comments_number_add() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
update public.posts set post_comments_number = post_comments_number+1 where post_id = NEW.post_id;
return NEW;
end;
$$;


ALTER FUNCTION public.post_comments_number_add() OWNER TO postgres;

--
-- TOC entry 217 (class 1255 OID 16860)
-- Name: post_comments_number_minus(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION post_comments_number_minus() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
update public.posts set post_comments_number = post_comments_number-1 where post_id = OLD.post_id;
return OLD;
end;
$$;


ALTER FUNCTION public.post_comments_number_minus() OWNER TO postgres;

--
-- TOC entry 206 (class 1255 OID 16861)
-- Name: post_likes_add(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION post_likes_add() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
update public.posts set likes = likes+1 where post_id = NEW.post_id;
return NEW;
end;
$$;


ALTER FUNCTION public.post_likes_add() OWNER TO postgres;

--
-- TOC entry 222 (class 1255 OID 16862)
-- Name: post_likes_minus(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION post_likes_minus() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
update public.posts set likes = likes-1 where post_id = OLD.post_id;
return OLD;
end;
$$;


ALTER FUNCTION public.post_likes_minus() OWNER TO postgres;

--
-- TOC entry 223 (class 1255 OID 16863)
-- Name: post_number_add(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION post_number_add() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
update public.user set posts_number = posts_number+1 where id = NEW.user_id;
return NEW;
end;
$$;


ALTER FUNCTION public.post_number_add() OWNER TO postgres;

--
-- TOC entry 215 (class 1255 OID 16864)
-- Name: post_number_minus(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION post_number_minus() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
update public.user set posts_number = posts_number-1 where id = OLD.user_id;
return OLD;
end;
$$;


ALTER FUNCTION public.post_number_minus() OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 196 (class 1259 OID 16865)
-- Name: comment_like; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE comment_like (
    user_id integer NOT NULL,
    comment_id integer NOT NULL,
    created_at timestamp with time zone
);


ALTER TABLE comment_like OWNER TO postgres;

--
-- TOC entry 197 (class 1259 OID 16868)
-- Name: comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE comments (
    user_id integer,
    post_id integer,
    comment_id integer NOT NULL,
    comment_type timestamp with time zone,
    comment_content text,
    likes integer
);


ALTER TABLE comments OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 16874)
-- Name: comments_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE comments_comment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE comments_comment_id_seq OWNER TO postgres;

--
-- TOC entry 2875 (class 0 OID 0)
-- Dependencies: 198
-- Name: comments_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE comments_comment_id_seq OWNED BY comments.comment_id;


--
-- TOC entry 199 (class 1259 OID 16876)
-- Name: post_like; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE post_like (
    user_id integer NOT NULL,
    post_id integer NOT NULL,
    created_at timestamp with time zone
);


ALTER TABLE post_like OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 16879)
-- Name: posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE posts (
    user_id integer,
    post_id integer NOT NULL,
    post_content text,
    post_time timestamp with time zone,
    likes integer,
    post_comments_number integer
);


ALTER TABLE posts OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 16885)
-- Name: posts_post_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE posts_post_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE posts_post_id_seq OWNER TO postgres;

--
-- TOC entry 2876 (class 0 OID 0)
-- Dependencies: 201
-- Name: posts_post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE posts_post_id_seq OWNED BY posts.post_id;


--
-- TOC entry 202 (class 1259 OID 16887)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE "user" (
    id integer NOT NULL,
    name text,
    email text,
    password text,
    gender text,
    phone text,
    created_at timestamp with time zone,
    user_region text,
    user_description text,
    posts_number integer,
    follow_number integer,
    follower_number integer
);


ALTER TABLE "user" OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 16893)
-- Name: user_follow; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE user_follow (
    user_follow_id integer NOT NULL,
    user_followed_id integer NOT NULL
);


ALTER TABLE user_follow OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 16896)
-- Name: user_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE user_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_user_id_seq OWNER TO postgres;

--
-- TOC entry 2877 (class 0 OID 0)
-- Dependencies: 204
-- Name: user_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE user_user_id_seq OWNED BY "user".id;


--
-- TOC entry 2709 (class 2604 OID 16898)
-- Name: comments comment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY comments ALTER COLUMN comment_id SET DEFAULT nextval('comments_comment_id_seq'::regclass);


--
-- TOC entry 2710 (class 2604 OID 16899)
-- Name: posts post_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY posts ALTER COLUMN post_id SET DEFAULT nextval('posts_post_id_seq'::regclass);


--
-- TOC entry 2711 (class 2604 OID 16900)
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "user" ALTER COLUMN id SET DEFAULT nextval('user_user_id_seq'::regclass);


--
-- TOC entry 2859 (class 0 OID 16865)
-- Dependencies: 196
-- Data for Name: comment_like; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY comment_like (user_id, comment_id, created_at) FROM stdin;
1	1	\N
1	2	\N
3	2	2017-11-12 07:17:31.673898+01
3	1	2017-11-12 07:17:32.692088+01
6	22	2017-11-12 08:05:01.923519+01
6	21	2017-11-12 08:05:24.715891+01
\.


--
-- TOC entry 2860 (class 0 OID 16868)
-- Dependencies: 197
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY comments (user_id, post_id, comment_id, comment_type, comment_content, likes) FROM stdin;
6	20	22	2017-11-12 08:04:54.724529+01	yolo lol	1
1	1	2	\N	allalal	2
1	1	1	\N	first comment	2
4	2	11	2017-11-11 17:30:29.939526+01	iop2 comment again	0
\.


--
-- TOC entry 2862 (class 0 OID 16876)
-- Dependencies: 199
-- Data for Name: post_like; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY post_like (user_id, post_id, created_at) FROM stdin;
1	1	\N
1	2	\N
3	1	2017-11-11 18:45:04.359124+01
6	20	2017-11-12 08:05:44.66371+01
\.


--
-- TOC entry 2863 (class 0 OID 16879)
-- Dependencies: 200
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY posts (user_id, post_id, post_content, post_time, likes, post_comments_number) FROM stdin;
6	20	hi yoann 2	2017-11-12 08:03:49.436745+01	1	1
1	1	my first post	\N	2	2
1	2	my second post	\N	1	1
\.


--
-- TOC entry 2865 (class 0 OID 16887)
-- Dependencies: 202
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "user" (id, name, email, password, gender, phone, created_at, user_region, user_description, posts_number, follow_number, follower_number) FROM stdin;
2	johnny2	johnny2@qq.com	asd12345	male	18811439786	\N	beijing	lalala	0	1	1
1	johnny	johnny@qq.com	asd12345	male	18811439786	\N	beijing	 no description	2	1	1
4	iop2	iop2@aaa.com	25d55ad283aa400af464c76d713c07ad	Male	0000000000	2017-11-11 17:25:54.186222+01			\N	\N	\N
5	iop3	iop3@mail.com	25d55ad283aa400af464c76d713c07ad	Male	0000000000	2017-11-12 07:46:28.364117+01	azeroth		\N	\N	\N
6	yoann	yoann@mail.com	a7c5937060ba4d4f077ed20b4c8b1e18	Male	0000000000	2017-11-12 07:52:59.918054+01			\N	\N	\N
3	iop	iop.iop@iop.cum	25d55ad283aa400af464c76d713c07ad	Female	0000000000	2017-11-11 13:14:07.950079+01	chinatown		\N	\N	\N
\.


--
-- TOC entry 2866 (class 0 OID 16893)
-- Dependencies: 203
-- Data for Name: user_follow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY user_follow (user_follow_id, user_followed_id) FROM stdin;
2	1
1	2
\.


--
-- TOC entry 2878 (class 0 OID 0)
-- Dependencies: 198
-- Name: comments_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('comments_comment_id_seq', 23, true);


--
-- TOC entry 2879 (class 0 OID 0)
-- Dependencies: 201
-- Name: posts_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('posts_post_id_seq', 21, true);


--
-- TOC entry 2880 (class 0 OID 0)
-- Dependencies: 204
-- Name: user_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('user_user_id_seq', 6, true);


--
-- TOC entry 2723 (class 2606 OID 16902)
-- Name: user_follow PK; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY user_follow
    ADD CONSTRAINT "PK" PRIMARY KEY (user_follow_id, user_followed_id);


--
-- TOC entry 2713 (class 2606 OID 16904)
-- Name: comment_like PK_commnet_like; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY comment_like
    ADD CONSTRAINT "PK_commnet_like" PRIMARY KEY (user_id, comment_id);


--
-- TOC entry 2715 (class 2606 OID 16906)
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (comment_id);


--
-- TOC entry 2717 (class 2606 OID 16908)
-- Name: post_like post_like_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY post_like
    ADD CONSTRAINT post_like_pkey PRIMARY KEY (user_id, post_id);


--
-- TOC entry 2719 (class 2606 OID 16910)
-- Name: posts post_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY posts
    ADD CONSTRAINT post_pk PRIMARY KEY (post_id);


--
-- TOC entry 2721 (class 2606 OID 16912)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 2726 (class 2620 OID 16913)
-- Name: comment_like comment_likes_add; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER comment_likes_add AFTER INSERT ON comment_like FOR EACH ROW EXECUTE PROCEDURE comment_likes_add();


--
-- TOC entry 2727 (class 2620 OID 16914)
-- Name: comment_like comment_likes_miunus; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER comment_likes_miunus AFTER DELETE ON comment_like FOR EACH ROW EXECUTE PROCEDURE comment_likes_minus();


--
-- TOC entry 2734 (class 2620 OID 16915)
-- Name: user_follow follow_add_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER follow_add_trigger AFTER INSERT ON user_follow FOR EACH ROW EXECUTE PROCEDURE follow_add();


--
-- TOC entry 2735 (class 2620 OID 16916)
-- Name: user_follow follow_minus_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER follow_minus_trigger AFTER DELETE ON user_follow FOR EACH ROW EXECUTE PROCEDURE follow_minus();


--
-- TOC entry 2736 (class 2620 OID 16917)
-- Name: user_follow follower_add_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER follower_add_trigger AFTER INSERT ON user_follow FOR EACH ROW EXECUTE PROCEDURE follower_add();


--
-- TOC entry 2737 (class 2620 OID 16918)
-- Name: user_follow follower_minus_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER follower_minus_trigger AFTER DELETE ON user_follow FOR EACH ROW EXECUTE PROCEDURE follower_minus();


--
-- TOC entry 2728 (class 2620 OID 16919)
-- Name: comments post_comments_number_add_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER post_comments_number_add_trigger AFTER INSERT ON comments FOR EACH ROW EXECUTE PROCEDURE post_comments_number_add();


--
-- TOC entry 2729 (class 2620 OID 16920)
-- Name: comments post_comments_number_minus_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER post_comments_number_minus_trigger AFTER DELETE ON comments FOR EACH ROW EXECUTE PROCEDURE post_comments_number_minus();


--
-- TOC entry 2730 (class 2620 OID 16921)
-- Name: post_like post_likes_add; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER post_likes_add AFTER INSERT ON post_like FOR EACH ROW EXECUTE PROCEDURE post_likes_add();


--
-- TOC entry 2731 (class 2620 OID 16922)
-- Name: post_like post_likes_minus; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER post_likes_minus AFTER DELETE ON post_like FOR EACH ROW EXECUTE PROCEDURE post_likes_minus();


--
-- TOC entry 2732 (class 2620 OID 16923)
-- Name: posts post_number_add; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER post_number_add AFTER INSERT ON posts FOR EACH ROW EXECUTE PROCEDURE post_number_add();


--
-- TOC entry 2733 (class 2620 OID 16924)
-- Name: posts post_number_minus; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER post_number_minus AFTER DELETE ON posts FOR EACH ROW EXECUTE PROCEDURE post_number_minus();


--
-- TOC entry 2724 (class 2606 OID 16925)
-- Name: comments comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- TOC entry 2725 (class 2606 OID 16930)
-- Name: comments post_foreign_key; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT post_foreign_key FOREIGN KEY (post_id) REFERENCES posts(post_id);


-- Completed on 2017-11-12 08:14:51

--
-- PostgreSQL database dump complete
--

