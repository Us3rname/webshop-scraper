from datetime import date, timedelta
import os

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2021, 1, 1)
end_date   = date(2021,1,2)
# end_date = date(2022, 11, 20)

for single_date in daterange(start_date, end_date):
    print(single_date.strftime("%Y-%m-%d"))

    cmd = "dbt run-operation prep_load --args '{load_date: single_date }'"
    # cmd = 'dbt run --select models/orchestration/truncate_stage.sql'
    os.system(cmd)

