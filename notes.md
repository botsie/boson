# Notes

## Dates
For consistency we may need a single set of dates that apply across the system. Need to decide:
* Just use a window and do roll ups in SQL
* Actually do it as tables

## How to do formulas
* ~~Perhaps use a trigger to update a column.~~
* ~~How to handle multiple formulas in a row? Programatically generate a PL/SQL function for the trigger?~~

## How to do rollups.
May have to become postgresql specific
1. Build a pivot using a crosstab query perhaps as a view
1. Use a ROLLUP to define the rollup.

## How to do trees
* Use a [closure table](https://gist.github.com/desfrenes/733a83ef82b03ee701caa761951767c9)
### Tree Operations thoughts
* build a temp table
* accumulate into that

## Misc Thoughts
* Need master detail views
* Need models for domain objects: Lists, Transactions, Documents , Reports, etc
* Will need to start storing metadata
* Lua, scheme or python for scripting?
* Use [postman](https://www.getpostman.com/postman) for API development.

## TODO
- [X] Convert to a postgresql back end
- [X] Use docker for postgres
- [ ] Implement formulas as views