CREATE TABLE sensors (
	id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name text NOT NULL UNIQUE,
	created_at timestamp with time zone DEFAULT now()
);
CREATE UNIQUE INDEX sensors_pkey ON sensors(id int4_ops);
CREATE UNIQUE INDEX sensors_name_key ON sensors(name);

CREATE TABLE parameters (
	id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name text NOT NULL UNIQUE,
	unit text NOT NULL,
	created_at timestamp with time zone NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX parameters_pkey ON parameters(id int4_ops);
CREATE UNIQUE INDEX parameters_name_key ON parameters(name);

CREATE TABLE sensor_parameters (
	sensor_id integer REFERENCES sensors(id) ON DELETE CASCADE,
	sensor_value integer,
	parameter_id integer REFERENCES parameters(id),
	CONSTRAINT sensor_parameters_pkey PRIMARY KEY (sensor_id, sensor_value)
);
CREATE UNIQUE INDEX sensor_parameters_pkey ON sensor_parameters(sensor_id int4_ops,sensor_value int4_ops);

CREATE TABLE measurements (
	device_address character varying(200),
	created_at timestamp with time zone DEFAULT now(),
	content double precision NOT NULL,
	parameter_id integer NOT NULL REFERENCES parameters(id),
	CONSTRAINT measurements_pkey PRIMARY KEY (created_at, device_address)
);
CREATE UNIQUE INDEX measurements_pkey ON measurements(created_at ,device_address);
SELECT create_hypertable('measurements', 'created_at');
