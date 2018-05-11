## This is a repository created for the Udacity Full Stack Nanodegree's Log Analysis Project.

## Before use:
You will need the news database provided with there course.
You will also need psycopyg2 for python3 installed.

## To use:
1. Run python3 ```python3```
2. Import the newsdata module ```import newsdata```
3. Run one of the 4 functions w/in the module  
    ex: ``newsdata.pop_articles("dbname")``  
    ex: ``newsdata.news_print("dbname","text.txt")``
4. Enjoy the results

## Functions:
#### pop_articles
Prints an ordered list of the most popular articles in the database
Returns a list of lists(article title, number of views)
#### pop_authors
Prints an ordered list of the most popular authors in the database
Returns a list of lists(author name, number of views)

#### most_errors
Prints a list of the days of the year that have more than 1% of total page views as errors.  
Retuns a list of lists(date, percentage)

#### news_print
Executes each of the above 3 functions.  
Saves the returns into a text file.

## Created views:
I created a couple of views to help out with this. They are used in the most_errors function
#### view errors:
create view errors as  
select date_trunc('days', time) as days, count(date_trunc('days', time)) as errors  
from log  
where status!='200 OK'  
group by days  
order by days;  


#### view daily_views:
create view daily_views as  
select date_trunc('days', time) as days, count(date_trunc('days', time)) as daily_views  
from log  
group by days  
order by days;  
