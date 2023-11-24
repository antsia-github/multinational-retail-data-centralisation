------Task 9-------------
WITH Ordertime AS
(select to_timestamp(concat(year,'-',month,'-',day,' ',timestamp), 'YYYY-MM-DD HH24:MI:SS') as order_time
from dim_date_times
ORDER BY order_time
), 

TwoTime AS 
(SELECT order_time, LEAD(order_time,1) OVER (ORDER BY order_time) next_order_time
FROM Ordertime
),

DiffTimeOrder AS
(SELECT order_time,next_order_time, DATE_PART('year', order_time) as year, DATE_PART('hour', next_order_time::timestamp - order_time::timestamp) as dhour,
               DATE_PART('minute', next_order_time::timestamp - order_time::timestamp) as dmin,
               DATE_PART('second', next_order_time::timestamp - order_time::timestamp) as dsec,
               DATE_PART('milliseconds', next_order_time::timestamp - order_time::timestamp) as dmsec
FROM TwoTime
),

AvgOrder AS
(SELECT year, concat(AVG(dhour),' hours ',AVG(dmin),' minutes ',AVG(dsec),' seconds ') AS dstamp 
FROM DiffTimeOrder
GROUP BY year
),


AvgTime AS
(SELECT year, EXTRACT(HOUR FROM dstamp::interval) as hour, EXTRACT(minute FROM dstamp::interval) as minute, EXTRACT(second FROM dstamp::interval) as seconds, EXTRACT(milliseconds FROM dstamp::interval) as milliseconds
FROM AvgOrder
ORDER BY hour, minute, seconds, milliseconds DESC
)

SELECT year, 
  concat('"hours": ',hour,', "minutes": ',minute,', "seconds": ',seconds,', "millise...') AS actual_time_taken 
FROM AvgTime
ORDER BY hour DESC, minute DESC, seconds DESC
LIMIT 7