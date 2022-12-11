{{ config(materialized='vault_insert_by_period', 
          timestamp_field='LOAD_DATE', period='day', 
          start_date='2021-12-01') }}

          
{%- set source_model = "v_stg_products_jumbo" -%}

{%- set src_pk = "PRODUCT_PK" -%}

{%- set src_hashdiff = {"source_column": "PRODUCT_PRICE_HASHDIFF",
                        "alias": "HASHDIFF"} -%}

{%- set src_payload = ["PRICE_AMOUNT", "UNIT", "UNIT_PRICE_AMOUNT"] -%}
{%- set src_eff = "EFFECTIVE_FROM" -%}
{%- set src_ldts = "LOAD_DATE" -%}
{%- set src_source = "RECORD_SOURCE" -%}


{{ dbtvault.sat(src_pk=src_pk, src_hashdiff=src_hashdiff, src_payload=src_payload,
                src_eff=src_eff, src_ldts=src_ldts, src_source=src_source,
                source_model=source_model)  }}