# Recommendation API server
this api server provides recommendary model(test)

## requirements
```
pymysql==1.0.2
flask
flask_cors
requests
```

`pip install -r requirements.txt`

## recommend_api.py

```
python recommend_api.py \
    -- port(optional) "port number(default 5001)" \
```


- operating api server in background : `python api.py ~~ %`
- terminating api server in background : `sh terminate_api.sh`
