# Getting Started

開啟前端伺服器，本機地址 [http://127.0.0.1:3000/](http://127.0.0.1:3000/)

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

# 頁面
## 已完成功能
* reg底下的頁面
    * [首頁](http://127.0.0.1:3000/uchi)
    * [登入頁面](http://127.0.0.1:3000/reg/login)
    * [忘記密碼](http://127.0.0.1:3000/reg/forgetpassword)
    * [註冊帳號](http://127.0.0.1:3000/reg/register)
    * [驗證信箱](http://127.0.0.1:3000/reg/valemail)
        > 註冊時會跳轉到此頁面，登入時未驗證也會。
        > <br/>若自己獲得連結可能會有bug
        > <br/><input type="checkbox" disabled> 修正，再不同瀏覽器開啟此頁面會導致驗證碼無法驗證到該帳號。
    * [驗證頁面](http://127.0.0.1:3000/reg/val?valdation_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im5lZG9nNTM2OTVAZ2VrbWUuY29tIiwidmFsMSI6MTM4OTI1LCJ2YWwyIjpmYWxzZSwiZXhwIjoxNjk3MDAyMjUyLCJpYXQiOjE2OTYzOTc0NTJ9.L5C7-FnJUhVUbvngScGQDEAzYPN9FWVrf9jWkQnV3dE)
        > 會再 http://127.0.0.1:3000/reg/val?valdation_token= 放入jwttoken用來驗證。 此連結會在使用者收到信時可以點擊。
* ifm 底下的頁面
    * [個人資料](http://127.0.0.1:3000/ifm)
    * [個人字卡](http://127.0.0.1:3000/ifm/card)
    * [修改資料](http://127.0.0.1:3000/ifm/remeishi)
* forum 底下的頁面
    * [討論區](http://127.0.0.1:3000/forum)
    * [討論區的頁面](http://127.0.0.1:3000/forum/1)
        > 看該篇文章的 id 大概是 http://127.0.0.1:3000/forum/[n]
    * [發送文章](http://127.0.0.1:3000/forum/send)
* billboard 底下的頁面
    * [公佈欄](http://127.0.0.1:3000/billboard)
    * [公佈欄的頁面](http://127.0.0.1:3000/billboard/1)
        > 看該篇文章的 id 大概是 http://127.0.0.1:3000/billboard/[n]
    * [發送公告](http://127.0.0.1:3000/billboard/send)
        > 若不據權限進入會自動跳轉至首頁
* study 底下的頁面
    * [學習中心](http://127.0.0.1:3000/study)
    * [英文字母](http://127.0.0.1:3000/study/english)
    * [測驗頁面](http://127.0.0.1:3000/study/testtype/1/q0)

## 未完成的
* [測驗結束頁面](http://127.0.0.1:3000/study/test/result)
* [線上聊天室](http://127.0.0.1:3000/study/test/onlinechat)
* [學習成果頁面](http://127.0.0.1:3000/study/test/result)


[]


