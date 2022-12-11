select  
  product.value:id::string as PRODUCT_ID,
  product.value:title::string as PRODUCT_TITLE,
  product.value:available::boolean as AVAILABLE,
  product.value:productType::string as PRODUCT_TYPE,
  product.value:nixProduct::string as NIX_PRODUCT,  
  product.value:sample::boolean as "SAMPLE",  
  product.value:quantity::string as QUANTITY,  
  product.value:prices:price:amount::int as PRICE_AMOUNT,    
  product.value:prices:unitPrice:unit::string as UNIT,  
  product.value:prices:unitPrice:price:amount::decimal as UNIT_PRICE_AMOUNT,    
  product.value:promotion:id::string as PROMOTION_ID,
  product.value:promotion:name::string as PROMOTION_NAME,
  product.value:promotion:fromDate::timestamp as PROMOTION_FROM_DATE,
  product.value:promotion:toDate::timestamp as PROMOTION_TO_DATE,
  product.value:promotion:validityPeriod::string as PROMOTION_VALIDITY_PERIOD,
  to_timestamp(substring(filename,charindex('response - ', filename) + 11, 19)) as FILE_CREATED_AT,
  'JUMBO' as SOURCE_SYSTEM  
  from    
    {{ source('webshop_scraper', 'stage_jumbo_webshop_products') }}
    , lateral flatten(input => file_content) request
    , lateral flatten(input => request.value:products:data) product