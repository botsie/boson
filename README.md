# Boson
A semantically addressed spreadsheet-like tool.

## Bootstrapping a dev environment
*Boson* depends on python 3. Here's a quick boostrap script for Mac OS X:

```bash
#!/bin/bash

brew install python3
cd $boson_src_dir
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt 
```

## Running the code
`database.yml` contains the database configuration. By default it uses the `development` 
environment. Override by setting a `BOSON_ENV` environment variable. 

Pass a yaml file as instructions to boson thus:

```bash
$ ./boson some_file.yml
```

Look at `script.yml` as a sample. You can run it like this:

```bash
$ ./boson script.yml
```
