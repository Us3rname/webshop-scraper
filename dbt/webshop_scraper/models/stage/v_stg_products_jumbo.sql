{{ config(materialized='view')}}

{%- set yaml_metadata -%}
source_model: 'raw_products_jumbo'

derived_columns:
  RECORD_SOURCE: 'RECORD_SOURCE'  
  LOAD_DATE: 'FILE_CREATED_AT'
  EFFECTIVE_FROM: 'FILE_CREATED_AT'

hashed_columns:
  PRODUCT_PK:
    - 'PRODUCT_ID'
    - 'RECORD_SOURCE'  
  PROMOTION_PK:
    - 'PROMOTION_ID'
    - 'RECORD_SOURCE'    
  PRODUCT_HASHDIFF:
    is_hashdiff: true
    columns:
      - 'PRODUCT_ID'
      - 'RECORD_SOURCE'
  PROMOTION_HASHDIFF:
    is_hashdiff: true
    columns:
      - 'PROMOTION_ID'
      - 'RECORD_SOURCE'

{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{% set source_model = metadata_dict['source_model'] %}

{% set derived_columns = metadata_dict['derived_columns'] %}

{% set hashed_columns = metadata_dict['hashed_columns'] %}

{{ dbtvault.stage(include_source_columns=true,
                  source_model=source_model,
                  derived_columns=derived_columns,
                  hashed_columns=hashed_columns,
                  ranked_columns=none) }}