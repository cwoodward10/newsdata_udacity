import psycopg2

# most popular articles of all time
# which articles have been accessed the most
# format:


def pop_articles(db_name):
    db = psycopg2.connect(dbname=db_name)
    c = db.cursor()
    # we want pages that don't result in errors, hence ='200 OK'
    # since all paths start w/ '/article/', can use like to compare to slug
    query = '''select articles.title, count(log.path) as views
                    from articles, log
                    where status='200 OK'
                    and log.path like '/article/'||articles.slug
                    group by articles.title
                    order by views desc;'''
    c.execute(query)
    rows = c.fetchall()
    db.close()
    for row in rows:
        result = '{} - {}'.format(row[0], row[1])
        print(result)
    return rows


# Who are the most popoular article authors of all time?
# which authors have the highest total aggregate views
# format: "Author-# views"

def pop_authors(db_name):
    db = psycopg2.connect(dbname=db_name)
    c = db.cursor()
    query = '''select authors.name, count(log.path) as views
                    from authors, articles, log
                    where status='200 OK'
                    and log.path like '/article/'||articles.slug
                    and authors.id=articles.author
                    group by authors.name
                    order by views desc;'''
    c.execute(query)
    rows = c.fetchall()
    db.close()
    for row in rows:
        result = '{} - {} views'.format(row[0], row[1])
        print(result)
    return rows

# On which days did more than 1% of requests lead to errors?
# Log tables that include error codes grouped by days
# format: "date-#% errors"


def most_errors(db_name):
    db = psycopg2.connect(dbname=db_name)
    c = db.cursor()
    # set up views that pulled total errors (code!=200) and total views per day
    # set upa subq to extract a percentage in way that where clause can be used
    query = '''select days, percentage
                from (select date(errors.days) as days,
                  round(((errors.errors / daily_views.daily_views::float)*100)
                  ::numeric,2) as percentage
                  from errors, daily_views
                  where errors.days=daily_views.days) as subq
                  where percentage>1;'''
    c.execute(query)
    rows = c.fetchall()
    db.close()
    for row in rows:
        result = '{} - {}% errors'.format(row[0], row[1])
        print(result)
    return rows

# Function to print out all 3 of the other function's outputs

def news_print(db_name, file_name):
    articles = pop_articles(db_name)
    authors = pop_authors(db_name)
    errors = most_errors(db_name)

    # I probably should have just made this its own function
    with open(file_name, mode='x') as f:
        f.write('Most Popular Articles\n')
        for article in articles:
            f.write('{} - {} views\n'.format(article[0], article[1]))
        f.write('\nMost Popular Authors\n')
        for author in authors:
            f.write('{} - {} views\n'.format(author[0], author[1]))
        f.write('\nDays with >1% of Views as Errors\n')
        for error in errors:
            f.write('{} - {} views\n'.format(error[0], error[1]))
