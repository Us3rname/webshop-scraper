{%- set yaml_metadata -%}
source_model: 'raw_products_jumbo'

derived_columns:
  RECORD_SOURCE: 'SOURCE_SYSTEM'  
  EFFECTIVE_FROM: 'FILE_CREATED_AT'
  LOAD_DATE: 'FILE_CREATED_AT'

hashed_columns:
  PRODUCT_PK:
    - 'PRODUCT_ID'
    - 'SOURCE_SYSTEM'  
  PROMOTION_PK:
    - 'PROMOTION_ID'
    - 'SOURCE_SYSTEM'    
  PRODUCT_DETAILS_HASHDIFF:
    is_hashdiff: true
    columns:
      - 'PRODUCT_ID'
      - 'SOURCE_SYSTEM'  
      - 'PRODUCT_TITLE'
  PRODUCT_PRICE_HASHDIFF:
    is_hashdiff: true
    columns:
      - 'PRODUCT_ID'
      - 'SOURCE_SYSTEM'  
      - 'PRICE_AMOUNT'
      - 'UNIT'
      - 'UNIT_PRICE_AMOUNT'      
  PROMOTION_HASHDIFF:
    is_hashdiff: true
    columns:
      - 'PROMOTION_ID'
      - 'PROMOTION_NAME'
      - 'PROMOTION_FROM_DATE'
      - 'PROMOTION_TO_DATE'
      - 'PROMOTION_VALIDITY_PERIOD'
      - 'SOURCE_SYSTEM'

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