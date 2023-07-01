python version: 3.11

deploy locally:

1) clone repo
```commandline
git clone https://github.com/phantom-profile/activities_manage_service.git
```

2) activate venv and install requirements
```commandline
# for Windows. If "python" command not found try "py" command
установка венва:
py -m venv venv

активация венва:
Set-ExecutionPolicy RemoteSigned -Scope Process
venv\Scripts\Activate.ps1
```

```commandline
# for Unix
python -m venv .
source venv/bin/activate
python -m pip install -r requirements.txt
```

```commandline
установка зависимостей
py -m pip install -r requirements.txt
```