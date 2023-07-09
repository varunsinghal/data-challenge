-- Specify the target year as a parameter
\set targetYear :targetYear

-- Insert records for each day of the target year
INSERT INTO dim_calendar (date, day, month, year)
SELECT
    date::DATE,
    EXTRACT(DAY FROM date) AS day,
    EXTRACT(MONTH FROM date) AS month,
    EXTRACT(YEAR FROM date) AS year
FROM
    generate_series(
        DATE_TRUNC('YEAR', TO_DATE(:targetYear::text, 'YYYY')),
        DATE_TRUNC('YEAR', TO_DATE(:targetYear::text, 'YYYY')) + INTERVAL '1 YEAR' - INTERVAL '1 DAY',
        INTERVAL '1 DAY'
    ) AS dates(date);
