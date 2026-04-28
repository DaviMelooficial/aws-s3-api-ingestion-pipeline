SELECT
    raw_data:userId::INT AS user_id,
    raw_data:id::INT AS post_id,
    raw_data:title::STRING AS title,
    raw_data:body::STRING AS body,
    source_file,
    loaded_at
FROM JSONPLACEHOLDER_PIPELINE_DB.RAW.JSONPLACEHOLDER_RAW