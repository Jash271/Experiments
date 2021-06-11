## Flask Serverless Deployment using Zappa Client

### Create Virtual Env

```
py -m pip install --user virtualenv
py -m venv env
.\env\Scripts\activate
```

### Install All dependenciesa and zappa in your Virtual Env and transfer them in requirements fie in Root Directory

```
pip freeze > requirements.txt
```

### Configure Zappa Client

```
zappa init
```

### Manage configurations in zappa_setting.json and give some project name i.e alpha

```
zappa deploy alpha
```

### Deployment Done,Test Endpoints
