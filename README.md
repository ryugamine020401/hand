# hand

# 套件版本
djangorestframework==3.14.0
  - django [required: >=3.0, installed: 3.2]
    - asgiref [required: >=3.3.2,<4, installed: 3.7.2]
      - typing-extensions [required: >=4, installed: 4.7.1]
    - pytz [required: Any, installed: 2023.3]
    - sqlparse [required: >=0.2.2, installed: 0.4.4]
  - pytz [required: Any, installed: 2023.3]
Pillow==10.0.0
PyJWT==2.8.0
PyMySQL==1.1.0
python-decouple==3.8


# 環境建立
透過pipenv管理虛擬環境，確認python版本3.8.10後安裝pipenv
```
pip install pipenv
```
安裝完成後在與pipnev檔案同目錄下輸入
```
pipenv shell
```
* 安裝相關套件
```
pipenv install
```
* 檢查套件
```
pipenv graph
```
* 

# Django使用
* 開啟伺服器
```
python manage.py runserver <port>
```
>　先到manage.py同目錄輸入(虛擬環境)

* 新增app
```
python manage.py startapp <app name>
```
* 建立資料遷移
```
python manage.py makemigration
```
* 資料遷移
```
python manage.py migrate
```

## 官方文件
- 檢索資料庫內的資料**Model.object.get()**、**Model.object.filter()** [https://docs.djangoproject.com/en/4.2/topics/db/queries/](官方文件)
  - filter出來的結果是Queryset
  - get是那個modles的實例。 
- 可以直接寫SQL語法**Model.object.raw(sql)** [https://docs.djangoproject.com/en/4.2/topics/db/sql/](官方文件)
