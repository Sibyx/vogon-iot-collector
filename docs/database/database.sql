-- Step 1: Create the Table

CREATE TABLE measurements (
	device_address character varying(200),
	pressure double precision,
	temperature double precision,
	humidity double precision,
	created_at timestamp with time zone,
	CONSTRAINT measurements_pkey PRIMARY KEY (created_at, device_address)
);

-- Step 2: Convert to Hypertable
SELECT create_hypertable('measurements', 'created_at');
