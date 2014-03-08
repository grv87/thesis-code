-- Схема базы данных
-- Database scheme
-- Copyright © 2013–2014  Василий Горохов-Апельсинов

-- This file is part of code for my bachelor's thesis.
--
-- Code for my bachelor's thesis is free software: you can redistribute
-- it and/or modify it under the terms of the GNU General Public License
-- as published by the Free Software Foundation, either version 3 of the
-- License, or (at your option) any later version.
--
-- Code for my bachelor's thesis is distributed in the hope that it will
-- be useful, but WITHOUT ANY WARRANTY; without even the implied
-- warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
-- the GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this code for my bachelor's thesis.  If not, see
-- <http://www.gnu.org/licenses/>.

-- Requirements: PostgreSQL (works with 9.2)

CREATE DOMAIN time_moment timestamptz(3);
CREATE DOMAIN time_interval interval(3);
CREATE DOMAIN price_type decimal(16, 5);
/* CREATE TYPE type AS ENUM (
	'ASK',
	'BID',
	'BEST_ASK',
	'BEST_BID',
	'TRADE'
); */
CREATE DOMAIN pieces_type decimal;

CREATE FUNCTION change(x2 time_moment, x1 time_moment) RETURNS time_interval
	LANGUAGE plpgsql IMMUTABLE RETURNS NULL ON NULL INPUT
AS $$
	BEGIN
		RETURN x2 - x1;
	END
$$;

CREATE FUNCTION change(x2 price_type, x1 price_type) RETURNS price_type
	LANGUAGE plpgsql IMMUTABLE RETURNS NULL ON NULL INPUT
AS $$
	BEGIN
		RETURN x2 - x1;
	END
$$;

CREATE FUNCTION ln_growth_rate(x2 anyelement, x1 anyelement) RETURNS double precision
	LANGUAGE plpgsql IMMUTABLE RETURNS NULL ON NULL INPUT
AS $$
	BEGIN
		-- Here we assume that '0' means '+0'
		IF sign(x2) * sign(x1) > 0 THEN
			RETURN ln(x2 / x1);
		ELSIF (x2 > 0) AND (x1 = 0) THEN
			RETURN 'Infinity'::double precision;
		ELSIF (x2 = 0) AND (x1 > 0) THEN
			RETURN '-Infinity'::double precision;
		ELSIF (x2 = 0) AND (x1 = 0) THEN
			RETURN 0; -- no growth
		ELSE -- sign(x2) * sign(x1) < 0
			RETURN 'NaN'::double precision;
		END IF;
	END
$$;

CREATE FUNCTION create_table(tablename name) RETURNS VOID
	LANGUAGE plpgsql VOLATILE RETURNS NULL ON NULL INPUT
AS $$
	BEGIN
		EXECUTE '
			CREATE TABLE '||quote_ident(tablename)||' (
				id bigserial PRIMARY KEY,
				moment time_moment NOT NULL,
				-- type type,
				price price_type NOT NULL CHECK (price > 0),
				volume pieces_type NOT NULL CHECK (volume > 0)
			);
	';
	END
$$;
