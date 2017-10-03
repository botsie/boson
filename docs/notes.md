# Notes

## Dates
For consistency we may need a single set of dates that apply across the system. Need to decide:
* Just use a window and do roll ups in SQL
* Actually do it as tables

## How to do formulas
* ~~Perhaps use a trigger to update a column.~~
* ~~How to handle multiple formulas in a row? Programatically generate a PL/SQL function for the trigger?~~
* Use views

## How to to do rules
* 'Rules' are procedures that happen in response to events like:
  * A table update
  * A cron execution
  * User trigger
* Need to validate whether they are really required. I want to avoid coding as much as possible. It might be sufficient to have formulas and rollups.
* May need to embed a scripting language:
  * Python
  * Lua
  * Scheme
* Python might be the easiest to do.
  

## How to do rollups.
* May have to become postgresql specific
* Build a pivot using a crosstab query perhaps as a view
  * But crosstabs require you to know the pivot headers in advance. :worried:
* Use a ROLLUP to define the rollup.
* Or we may have to do it in python and take the performance hit.

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
- [ ] Write some design documentation
- [ ] Implement formulas as views
- [ ] Move logic from task classes to models
- [ ] Write a print task
- [ ] Write a CSV import task
- [ ] Add a date range as metadata

