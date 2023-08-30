# hand
# 環境建立
透過pipenv管理虛擬環境，確認python版本3.8.10後安裝pipenv
```
pip install pipenv
```
安裝完成後在與pipnev檔案同目錄下輸入
```
pipenv shell
```
- 安裝相關套件
```
pipenv install
```
- 檢查套件
```
pipenv graph
```
# 設定.env 
找到.env.example進去修改，根據內容修改成主機上的相關port跟其他內容。
```
EMAIL_HOST_USER = 發送驗證信的email
ROOT_EMAIL = root帳號，開啟後需要註冊
EMAIL_HOST_PASSWORD=[google用django寄信](https://www.youtube.com/watch?v=YQboCnlOb6Y)
DB_NAME=主機內的mysql資料庫名稱
DB_PASSWORD=資料庫密碼
DB_PORT=資料庫開的port預設是3306
SECRET_KEY=密鑰1
JWT_ACCRSS_TOKEN_KEY=密鑰2
JWT_REFRESH_TOKEN_KEY=密鑰3
DEBUG=True
```

# Django使用
進入環境後到hand目錄底下(同manage.py)。
- 開啟伺服器
```
python manage.py runserver <port>
```
>　先到manage.py同目錄輸入(虛擬環境) port可設可不設 預設是8000
>  - 正常開啟後可以看到，到瀏覽器輸入 [http://127.0.0.1:8000](http://127.0.0.1:8000) 可進入網站
>  - ![image](https://github.com/ryugamine020401/hand/assets/67624967/9f53d6ae-06d1-4a59-83ef-6358db22dca7)
>  <br> 在.env有設定好的情況下可以直接看到所有可用的url



- 新增app
```
python manage.py startapp <app name>
```
- 建立資料遷移
```
python manage.py makemigration
```
- 資料遷移
```
python manage.py migrate
```

## 官方文件
- 檢索資料庫內的資料**Model.object.get()**、**Model.object.filter()** [https://docs.djangoproject.com/en/4.2/topics/db/queries/](官方文件)
  - filter出來的結果是Queryset
  - get是那個modles的實例。 
- 可以直接寫SQL語法**Model.object.raw(sql)** [https://docs.djangoproject.com/en/4.2/topics/db/sql/](官方文件)

# 完成進度
## 前端

## 後端

# 套件版本
**channels-redis==4.1.0**
  - asgiref [required: >=3.2.10,<4, installed: 3.7.2]
    - typing-extensions [required: >=4, installed: 4.7.1]
  - channels [required: Any, installed: 3.0.5]
    - asgiref [required: >=3.5.0,<4, installed: 3.7.2]
      - typing-extensions [required: >=4, installed: 4.7.1]
    - daphne [required: >=3.0,<4, installed: 3.0.2]
      - asgiref [required: >=3.2.10,<4, installed: 3.7.2]
        - typing-extensions [required: >=4, installed: 4.7.1]
      - autobahn [required: >=0.18, installed: 23.1.2]
        - cryptography [required: >=3.4.6, installed: 41.0.3]
          - cffi [required: >=1.12, installed: 1.15.1]
            - pycparser [required: Any, installed: 2.21]
        - hyperlink [required: >=21.0.0, installed: 21.0.0]
          - idna [required: >=2.5, installed: 3.4]
        - setuptools [required: Any, installed: 68.1.2]
        - txaio [required: >=21.2.1, installed: 23.1.1]
      - twisted [required: >=18.7, installed: 22.10.0]
        - attrs [required: >=19.2.0, installed: 23.1.0]
        - Automat [required: >=0.8.0, installed: 22.10.0]
          - attrs [required: >=19.2.0, installed: 23.1.0]
          - six [required: Any, installed: 1.16.0]
        - constantly [required: >=15.1, installed: 15.1.0]
        - hyperlink [required: >=17.1.1, installed: 21.0.0]
          - idna [required: >=2.5, installed: 3.4]
        - incremental [required: >=21.3.0, installed: 22.10.0]
        - typing-extensions [required: >=3.6.5, installed: 4.7.1]
        - zope.interface [required: >=4.4.2, installed: 6.0]
          - setuptools [required: Any, installed: 68.1.2]
    - Django [required: >=2.2, installed: 3.2]
      - asgiref [required: >=3.3.2,<4, installed: 3.7.2]
        - typing-extensions [required: >=4, installed: 4.7.1]
      - pytz [required: Any, installed: 2023.3]
      - sqlparse [required: >=0.2.2, installed: 0.4.4]
  - msgpack [required: ~=1.0, installed: 1.0.5]
  - redis [required: >=4.5.3, installed: 5.0.0]
    - async-timeout [required: >=4.0.2, installed: 4.0.3]

**djangorestframework==3.14.0**
  - django [required: >=3.0, installed: 3.2]
    - asgiref [required: >=3.3.2,<4, installed: 3.7.2]
      - typing-extensions [required: >=4, installed: 4.7.1]
    - pytz [required: Any, installed: 2023.3]
    - sqlparse [required: >=0.2.2, installed: 0.4.4]
  - pytz [required: Any, installed: 2023.3]

**mediapipe==0.9.3.0**
  - absl-py [required: Any, installed: 1.4.0]
  - attrs [required: >=19.1.0, installed: 23.1.0]
  - flatbuffers [required: >=2.0, installed: 23.5.26]
  - matplotlib [required: Any, installed: 3.7.2]
    - contourpy [required: >=1.0.1, installed: 1.1.0]
      - numpy [required: >=1.16, installed: 1.24.4]
    - cycler [required: >=0.10, installed: 0.11.0]
    - fonttools [required: >=4.22.0, installed: 4.42.0]
    - importlib-resources [required: >=3.2.0, installed: 6.0.1]
      - zipp [required: >=3.1.0, installed: 3.16.2]
    - kiwisolver [required: >=1.0.1, installed: 1.4.4]
    - numpy [required: >=1.20, installed: 1.24.4]
    - packaging [required: >=20.0, installed: 23.1]
    - pillow [required: >=6.2.0, installed: 10.0.0]
    - pyparsing [required: >=2.3.1,<3.1, installed: 3.0.9]
    - python-dateutil [required: >=2.7, installed: 2.8.2]
      - six [required: >=1.5, installed: 1.16.0]
  - numpy [required: Any, installed: 1.24.4]
  - opencv-contrib-python [required: Any, installed: 4.8.0.76]
    - numpy [required: >=1.17.3, installed: 1.24.4]
    - numpy [required: >=1.17.0, installed: 1.24.4]
  - protobuf [required: >=3.11,<4, installed: 3.20.3]
  - sounddevice [required: >=0.4.4, installed: 0.4.6]
    - CFFI [required: >=1.0, installed: 1.15.1]
      - pycparser [required: Any, installed: 2.21]

**PyJWT==2.8.0**

**PyMySQL==1.1.0**

**pyOpenSSL==23.2.0**
  - cryptography [required: >=38.0.0,<42,!=40.0.1,!=40.0.0, installed: 41.0.3]
    - cffi [required: >=1.12, installed: 1.15.1]
      - pycparser [required: Any, installed: 2.21]

**python-decouple==3.8**

**service-identity==23.1.0**
  - attrs [required: >=19.1.0, installed: 23.1.0]
  - cryptography [required: Any, installed: 41.0.3]
    - cffi [required: >=1.12, installed: 1.15.1]
      - pycparser [required: Any, installed: 2.21]
  - pyasn1 [required: Any, installed: 0.5.0]
  - pyasn1-modules [required: Any, installed: 0.3.0]
    - pyasn1 [required: >=0.4.6,<0.6.0, installed: 0.5.0]


# 目錄架構
```markdown
hand
|
|---billboard
|           |---__pycache__
|           |---migrations
|           |---templates
|           |---__init__.py
|           |---admin.py
|           |---apps.py
|           |---forms.py
|           |---models.py
|           |---tests.py
|           |---urls.py
|           |---views.py
|---bugreport
|           |---約同billboard
|---forum
|           |---約同billboard
|---hand
|           |---__pycache__
|           |---__init__.py
|           |---asgi.py
|           |---settings.py
|           |---urls.py
|           |---wsgi.py
|---ifm
|           |---__pycache__
|           |---migrations
|           |---templates
|           |---__init__.py
|           |---admin.py
|           |---apps.py
|           |---forms.py
|           |---models.py
|           |---serializers.py
|           |---tests.py
|           |---urls.py
|           |---views.py
|---media
|           |---headimage
|           |           |---defaultimage.png
|           |---studyimage
|           |           |---english
|           |           |          |---A.png
|           |           |          |---B.png
|           |           |          |---...
|---onlinechat
|           |---__pycache__
|           |---migrations
|           |---templates
|           |---__init__.py
|           |---admin.py
|           |---apps.py
|           |---consumers.py
|           |---forms.py
|           |---models.py
|           |---routing.py
|           |---serializers.py
|           |---tests.py
|           |---urls.py
|           |---views.py
|---reg
|           |---__pycache__
|           |---migrations
|           |---templates
|           |---__init__.py
|           |---admin.py
|           |---apps.py
|           |---forms.py
|           |---models.py
|           |---serializers.py
|           |---tests.py
|           |---urls.py
|           |---views.py
|---static
|           |---css
|           |           |---lobby.css
|---study
|           |---__pycache__
|           |---migrations
|           |---templates
|           |---__init__.py
|           |---admin.py
|           |---apps.py
|           |---forms.py
|           |---models.py
|           |---serializers.py
|           |---tests.py
|           |---urls.py
|           |---views.py
|---.env
|---.gitignore
|---db.sqlite3
|---manage.py
Pipenv
Pipenv.lock
README.md
```
