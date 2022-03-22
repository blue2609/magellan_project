CREATE DATABASE sftp_db;
\connect sftp_db 
CREATE TABLE IF NOT EXISTS index_files (
	filename TEXT PRIMARY KEY,
	filesize INT NOT NULL,
	last_modified_time INT NOT NULL
);

CREATE TABLE IF NOT EXISTS index_file_changes_log (
	id SERIAL PRIMARY KEY,
	filename TEXT NOT NULL,
	datetime TIMESTAMPTZ NOT NULL,
	operation_type TEXT NOT NULL,
	old_mtime INT,
	new_mtime INT NOT NULL, 
	old_size INT, 
	new_size INT NOT NULL
);

-- Create trigger for INSERT and UPDATE operation
CREATE OR REPLACE FUNCTION fn_detect_file_insert_or_update()
	RETURNS TRIGGER 
	LANGUAGE PLPGSQL
	AS
$$
BEGIN
	if tg_op = 'UPDATE'	then
		INSERT INTO index_file_changes_log (
			filename, 
			datetime, 
			operation_type, 
			old_mtime, 
			new_mtime, 
			old_size, 
			new_size
		)
		VALUES (
			NEW.filename, 
			NOW(), 
			tg_op, 
			OLD.last_modified_time, 
			NEW.last_modified_time, 
			OLD.filesize, 
			NEW.filesize
		);
		perform pg_notify('file_updated', 
			json_build_object(
				'operation_type', tg_op,
				'filename', NEW.filename
			)::text
		);
	elsif tg_op = 'INSERT' then
		INSERT INTO index_file_changes_log (
			filename, 
			datetime, 
			operation_type, 
			new_mtime, 
			new_size
		)
		VALUES (
			NEW.filename, 
			NOW(), 
			tg_op, 
			NEW.last_modified_time, 
			NEW.filesize
		);
		perform pg_notify('new_file_added', 
			json_build_object(
				'operation_type', tg_op,
				'filename', NEW.filename
			)::text
		);
	end if;
	RETURN NEW;
END;
$$;

-- Attach trigger to table 'index_files'
CREATE TRIGGER trg_detect_file_insert_or_update
	AFTER INSERT OR UPDATE
ON index_files
	FOR EACH ROW
	EXECUTE PROCEDURE fn_detect_file_insert_or_update();



