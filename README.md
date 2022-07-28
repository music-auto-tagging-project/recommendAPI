# Recommendation API server
this api server provides recommendary model

## requirements
```
pymysql==1.0.2
flask
flask_cors
```

`pip install -r requirements.txt`

## api.py
Because this api server accesses DB server, **should give some information to login DB.**

```
python api.py \
    --host "db server endpoint" \
    --user "user id to login DB" \
    --db "DB name to be accessed" \
    --password "user password to login DB" \
    -- port(optional) "port number(default 5001)" \
```


- operating api server in background : `python api.py ~~ %`
- terminating api server in background : `sh terminate_api.sh`