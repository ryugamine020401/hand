# 使用官方的 Python 3.8.10 映像作為基礎
FROM python:3.8.10

# 在容器中創建應用程式的工作目錄
WORKDIR /backend

# 安裝必要的系統套件，包括 libGL.so.1
RUN apt-get update && apt-get install -y libgl1-mesa-glx && apt install nano

# 複製應用程式的程式碼到容器中
COPY . .

RUN pip install pipenv

CMD ["/bin/bash", "-c", "pipenv install --deploy --ignore-pipfile && cd /backend/hand/ && pipenv run python manage.py runserver 0.0.0.0:8000"]
# CMD ["pipenv", "install", "--deploy", "--ignore-pipfile"]