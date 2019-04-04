# Notes

## Dates
* neo4j dates plugin

## How to do formulas
* save in metadata
* calculate when reporting

## How to to do rules
* ??

## How to do rollups.
* sum up the hierarchy



## How to do trees
* Use a [closure table](https://gist.github.com/desfrenes/733a83ef82b03ee701caa761951767c9)
### Tree Operations thoughts
* build a temp table
* accumulate into that
* Build a bottom up traversal and top down traveral methods that accept parameterized formulas.

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

