CREATE DATABASE archive_db;
\connect archive_db 
CREATE TABLE IF NOT EXISTS archived_cls (
	id VARCHAR(13) PRIMARY KEY,
	index_name TEXT NOT NULL,
	index_code VARCHAR(10) NOT NULL,
	index_key TEXT NOT NULL,
	effective_date CHAR(8) NOT NULL, 
	company TEXT NOT NULL,
	ric VARCHAR(8) NOT NULL,
	bloomberg_ticker VARCHAR(8) NOT NULL,
	cusip TEXT, 
	isin CHAR(12) NOT NULL,
	sedol TEXT,
	ticker VARCHAR(5) NOT NULL,
	gv_key CHAR(9) NOT NULL,
	stock_key TEXT NOT NULL,
	gics_code CHAR(8) NOT NULL,
	dji_industry_code CHAR(17) NOT NULL,
	alternate_classification_code TEXT,
	mic TEXT NOT NULL,
	country_of_domicile VARCHAR(3) NOT NULL,
	country_of_listing VARCHAR(3) NOT NULL,
	region TEXT,
	size TEXT,
	cap_range TEXT,
	currency_code CHAR(3) NOT NULL,
	local_price FLOAT NOT NULL,
	fx_rate INT NOT NULL,
	shares_outstanding BIGINT NOT NULL,
	market_cap FLOAT NOT NULL,
	iwf FLOAT NOT NULL,
	awf INT NOT NULL,
	growth FLOAT NOT NULL,
	value FLOAT NOT NULL,
	index_shares FLOAT NOT NULL,
	index_market_cap FLOAT NOT NULL,
	index_weight FLOAT NOT NULL,
	daily_price_return FLOAT NOT NULL,
	daily_total_return FLOAT NOT NULL,
	dividend FLOAT,
	net_dividend FLOAT		
);

-- CREATE TABLE IF NOT EXISTS index_file_changes_log (
-- 	id SERIAL PRIMARY KEY,
-- 	filename TEXT NOT NULL,
-- 	datetime TIMESTAMPTZ NOT NULL,
-- 	operation_type TEXT NOT NULL,
-- 	old_mtime INT,
-- 	new_mtime INT NOT NULL, 
-- 	old_size INT, 
-- 	new_size INT NOT NULL
-- );

-- -- Create trigger for update operation
-- CREATE OR REPLACE FUNCTION fn_detect_file_insert_or_update()
-- 	RETURNS TRIGGER 
-- 	LANGUAGE PLPGSQL
-- 	AS
-- $$
-- BEGIN
-- 	if tg_op = 'UPDATE'	then
-- 		INSERT INTO index_file_changes_log (
-- 			filename, 
-- 			datetime, 
-- 			operation_type, 
-- 			old_mtime, 
-- 			new_mtime, 
-- 			old_size, 
-- 			new_size
-- 		)
-- 		VALUES (
-- 			NEW.filename, 
-- 			NOW(), 
-- 			tg_op, 
-- 			OLD.last_modified_time, 
-- 			NEW.last_modified_time, 
-- 			OLD.filesize, 
-- 			NEW.filesize
-- 		);
-- 		perform pg_notify('file_updated', 
-- 			json_build_object(
-- 				'operation_type', tg_op,
-- 				'filename', NEW.filename
-- 			)::text
-- 		);
-- 	elsif tg_op = 'INSERT' then
-- 		INSERT INTO index_file_changes_log (
-- 			filename, 
-- 			datetime, 
-- 			operation_type, 
-- 			new_mtime, 
-- 			new_size
-- 		)
-- 		VALUES (
-- 			NEW.filename, 
-- 			NOW(), 
-- 			tg_op, 
-- 			NEW.last_modified_time, 
-- 			NEW.filesize
-- 		);
-- 		perform pg_notify('new_file_added', 
-- 			json_build_object(
-- 				'operation_type', tg_op,
-- 				'filename', NEW.filename
-- 			)::text
-- 		);
-- 	end if;
-- 	RETURN NEW;
-- END;
-- $$;

-- CREATE TRIGGER trg_detect_file_insert_or_update
-- 	AFTER INSERT OR UPDATE
-- ON index_files
-- 	FOR EACH ROW
-- 	EXECUTE PROCEDURE fn_detect_file_insert_or_update();



