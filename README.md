# Top Articles

The top articles parser is a solution to a training ParseKit assignment offered in the ParseKit support docs. This parser highlights how to merge records from different sources into one table. It also demonstrates how to correctly perform joins. Enigma strongly recommends against joining data during the ingestion phase. Generally a data management platform such as Enigma's Abstract is the best place to perform first class data operations. However, in the rare case such functionality is necessary, it is idiomatic to perform joins in an intermediate data store, such as SQLite. ParseKit itself does not perform joins.

This parser was created to collect the data necessary to answer the question,
"Do the most popular articles shared on reddit & hackernews, come from the most 
popular online publishers?" 

## Installation

### Setup Dependencies:
`pip install -r requirements.txt`

### Run
`parsekit run --allow-unsafe`

Allow unsafe is needed because modifying string transformations are used on certain data fields. 

## Parsing Strategy

The parser aggregates the top links on Hackernews and Reddit.com/r/programming. Two seperate pipelines extract the article title, url and points for HN and reddit articles respectively. Another pipeline is used to scrape ebizmba.com's rankings of the top trafficed websites.  Each of these datasets is pushed to a table in a cacheing warehouse `cache.db`. This db is placed in the working directory so that it is deleted after each run.

In the final pipeline, the HackerNews and Reddit tables are appended onto each other and then joined with the top traffic list to extract the final dataset. The join with the top trafficed sites allows the creation of a field that indicates whether or not the article comes from a top trafficed site. The results are stored in a seperate DB called `results.db`. A seperate SQLite DB needed to be used because SQLite locking prevents the user from creating tables and reading records off the same DB at the exact same time. Other DBs may or may not have similar restrictions and its up to users to understand any edge cases.

## Datasource Notes
Reddit upvote strings sometimes have characters that python struggles to coerce. So coercion to integers is handled by SQLite.

## Further Notes
The user could run this parser every hour if they wanted to track the movements of articles(in terms of points) over time. The user would simply need to change the primary key of the result table to also include the date. That way each update to an article would be stored in the DB. The ParseKit Platform offered by Enigma is the best tool for scheduling and monitoring such a process. 
