{% docs get_date_id %}
This creates a conformed date_id for use in with the date dimension in common. This macro should always be used when the output for a column is meant to join with date_id in the date dimension. This macro does not include an alias so an alias must always be applied. 
{% enddocs %}

{% docs dbt_audit %}
Used to append audit columns to a model.

This model assumes that the final statement in your model is a `SELECT *` from a CTE. The final SQL will still be a `SELECT *` just with 6 additional columns added to it. Further SQL DML can be added after the macro call, such as ORDER BY and GROUP BY.

There are two internally calculated date values based on when the table is created and, for an incremental model, when data was inserted.

```sql
WITH my_cte AS (...)
{% raw %}
{{ dbt_audit(
    cte_ref="my_cte", 
    created_by="@gitlab_user1", 
    updated_by="@gitlab_user2", 
    created_date="2019-02-12", 
    updated_date="2020-08-20"
) }}
{% endraw %}
ORDER BY updated_at
```

{% enddocs %}