python version: 3.11

deploy locally:

1) clone repo
```commandline
git clone repo_name
```

2) install requirements

```commandline
python -m pip install -r requirements.txt
```

3) run migrations
```commandline
python migrate.py
```

4) run application
```commandline
flask --app app/main run --debug
```
