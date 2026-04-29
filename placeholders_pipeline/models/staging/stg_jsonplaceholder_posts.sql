WITH source AS (
    SELECT
        raw_data:userId::INT AS user_id,
        raw_data:id::INT AS post_id,
        raw_data:title::STRING AS title,
        raw_data:body::STRING AS body,
        source_file,
        loaded_at
    FROM {{ source('raw', 'jsonplaceholder_raw') }}
),

deduplicated AS (
    SELECT
        *
    FROM source
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY post_id
        ORDER BY loaded_at DESC, source_file DESC
    ) = 1
)

SELECT *
FROM deduplicated