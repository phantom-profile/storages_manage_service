python version: 3.11

deploy locally:

1) clone repo
```commandline
git clone https://github.com/phantom-profile/activities_manage_service.git
```

2) install requirements

```commandline
python -m pip install -r requirements.txt
```

3) run migrations
```commandline
python migrate.py
```
te
4) run application
```commandline
flask --app app/main run --debug
```

