# 使用官方的 Node.js 映像作為基礎
FROM node:18.17.1

# 在容器中創建應用程式的工作目錄
WORKDIR /frontend

# 複製 package.json 和 package-lock.json 到容器中，以便安裝相依套件
COPY package*.json ./

# 安裝相依套件
RUN npm install

# 複製應用程式程式碼到容器中
COPY . .

# 啟動應用程式
CMD [ "npm", "run", "dev" ]