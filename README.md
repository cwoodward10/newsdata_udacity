

#### view errors:
create view errors as
select date_trunc('days', time) as days, count(date_trunc('days', time)) as errors
from log
where status!='200 OK'
group by days
order by days;


### view daily_views:
create view daily_views as
select date_trunc('days', time) as days, count(date_trunc('days', time)) as daily_views
from log
group by days
order by days;
