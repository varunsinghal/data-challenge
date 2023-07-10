begin;

CREATE TABLE IF NOT EXISTS dim_country (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS dim_currency (
    currency_id SERIAL PRIMARY KEY,
    currency_code VARCHAR(3),
    currency_name VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS map_country_currency (
    map_country_currency_id SERIAL PRIMARY KEY,
    country_id INTEGER REFERENCES dim_country(country_id),
    currency_id INTEGER REFERENCES dim_currency(currency_id)
);


CREATE TABLE IF NOT EXISTS dim_calendar (
    date_id BIGSERIAL PRIMARY KEY,
    date DATE,
    day INTEGER,
    month INTEGER,
    year INTEGER
);


CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id BIGSERIAL PRIMARY KEY,
    country_id INT REFERENCES dim_country(country_id),
    customer_age INT,
    customer_gender VARCHAR(50)
);

CREATE INDEX idx_customer_country_id ON dim_customer (country_id);


CREATE TABLE IF NOT EXISTS fact_transaction (
    transaction_id bigserial PRIMARY KEY,
    customer_id bigint REFERENCES dim_customer(customer_id), 
    transaction_type int,
    amount decimal,
    currency_id int REFERENCES dim_currency(currency_id),
    date_id bigint REFERENCES dim_calendar(date_id)
);

CREATE INDEX idx_transaction_customer_id ON fact_transaction (customer_id);
CREATE INDEX idx_transaction_date_id ON fact_transaction (date_id);
CREATE INDEX idx_transaction_currency_id ON fact_transaction (currency_id);
CREATE INDEX idx_transaction_transaction_type_id ON fact_transaction (transaction_type);



CREATE TABLE IF NOT EXISTS fact_exchange_rate (
    exchange_rate_id bigserial PRIMARY KEY,
    from_currency_id int REFERENCES dim_currency(currency_id),
    to_currency_id int REFERENCES dim_currency(currency_id),
    effective_date_id bigint REFERENCES dim_calendar(date_id),
    rate decimal
);

CREATE INDEX idx_exchange_rate_date_id ON fact_exchange_rate (effective_date_id);
CREATE INDEX idx_exchange_rate_source_currency_id ON fact_exchange_rate (from_currency_id);
CREATE INDEX idx_exchange_rate_target_currency_id ON fact_exchange_rate (to_currency_id);



CREATE TABLE IF NOT EXISTS staging_customer (
    row_id BIGSERIAL PRIMARY KEY,
    customer_id bigint,
    country text,
    customer_age text,
    customer_gender text,
    error_message text
);

CREATE TABLE IF NOT EXISTS staging_transaction (
    row_id BIGSERIAL PRIMARY KEY,
    transaction_id bigint,
    customer_id	text, 
    transaction_type text, 
    amount text, 
    currency text, 
    transaction_date text,
    error_message text
);

CREATE TABLE IF NOT EXISTS staging_exchange_rate (
    row_id BIGSERIAL PRIMARY KEY,
    exchange_rate_id bigint,
    from_currency text, 
    to_currency text,
    effective_date text,
    rate text,
    error_message text
);

/*
 * Views
 */

create or replace
view transaction_summary_view as
select 
	count(customer_id) as unique_customers,
	sum(count_transaction) as total_transactions,
	sum(amount) as total_amount,
	month,
	year
from
	(
	select
		dc.customer_id,
		count(ft.transaction_id) as count_transaction,
		sum((ft.amount / fer.rate)* fer2.rate) as amount,
		cal."month" ,
		cal."year"
	from
		fact_transaction ft
	inner join dim_calendar cal on
		ft.date_id = cal.date_id
	inner join dim_customer dc on
		dc.customer_id = ft.customer_id
	inner join dim_country dc2 on
		dc.country_id = dc2.country_id
	inner join fact_exchange_rate fer on
		fer.effective_date_id = ft.date_id
		and fer.to_currency_id = ft.currency_id
	inner join fact_exchange_rate fer2 on
		fer2.effective_date_id = ft.date_id
	inner join dim_currency from_currency 
	on
		fer2.from_currency_id = from_currency.currency_id
		and from_currency.currency_code = 'GBP'
	inner join dim_currency to_currency 
	on
		fer2.to_currency_id = to_currency.currency_id
		and to_currency.currency_code = 'EUR'
	group by
		dc.customer_id,
		cal.month,
		cal.year,
		dc2.country_name 
		) A
group by 
	month,
	year ;



CREATE OR REPLACE VIEW exchange_rate_view AS
select
	dc2.currency_code,
	cal.date,
	cal.date_id,
	rate,
	rate_next_day,
	((rate_next_day - rate) / rate) * 100 as percentage_change
from
	(
	select
		to_currency_id,
		effective_date_id,
		rate,
		lead(rate, 1) over (partition by to_currency_id
	order by
		effective_date_id) as rate_next_day
	from
		fact_exchange_rate fer
		)
       as A
inner join dim_currency dc2 on
	dc2.currency_id = A.to_currency_id
inner join dim_calendar cal on 
	cal.date_id = A.effective_date_id
where dc2.currency_code <> 'GBP';



end;