# 切換到後端開啟伺服器的目錄
cd ./baekend/hand
# 自動檢測虛擬環境的路徑
VENV_PATH=$(pipenv --venv)
sudo redis-server &
source "$VENV_PATH/bin/activate"
python manage.py runserver &
# nohup python manage.py runserver >/dev/null 2>&1 &
# 退回專案的根路徑
cd ../../

# 切換到前端目錄
cd ./frontend

npm run dev


