SELECT
    user_id,
    COUNT(*) AS total_posts,
    AVG(LENGTH(title)) AS avg_title_length,
    MAX(loaded_at) AS last_loaded
FROM {{ ref('stg_jsonplaceholder_posts') }}
GROUP BY user_id