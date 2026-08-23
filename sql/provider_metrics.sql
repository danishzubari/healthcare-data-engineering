-- Analytics examples for the standardized provider dataset.
-- The Python pipeline materializes equivalent dashboard aggregates.

SELECT
    state,
    COUNT(*) AS provider_count
FROM providers
GROUP BY state
ORDER BY provider_count DESC;

SELECT
    pri_spec AS specialty,
    COUNT(*) AS provider_count
FROM providers
GROUP BY pri_spec
ORDER BY provider_count DESC;

SELECT
    telehlth AS telehealth_indicator,
    COUNT(*) AS provider_count
FROM providers
GROUP BY telehlth
ORDER BY provider_count DESC;
