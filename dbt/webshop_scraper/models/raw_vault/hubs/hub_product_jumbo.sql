{{ config(materialized='vault_insert_by_period', 
          timestamp_field='LOAD_DATE', period='day', 
          start_date='2021-12-01') }}

{%- set source_model = "v_stg_products_jumbo" -%}

{%- set src_pk = "PRODUCT_PK" -%}
{%- set src_nk = ["PRODUCT_ID", "SOURCE_SYSTEM"] -%}
{%- set src_source = "RECORD_SOURCE" -%}
{%- set src_ldts = "LOAD_DATE" -%}

{{ dbtvault.hub(src_pk=src_pk, src_nk=src_nk, src_ldts=src_ldts,
                src_source=src_source, source_model=source_model) }}