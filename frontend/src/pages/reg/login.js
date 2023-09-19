import Head from "next/head";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/router"; // 導入 useRouter
import Link from "next/link";

export default function Ifm({ data, done, access_token, refresh_token }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState(""); 
  const router = useRouter(); // 初始化 useRouter

  useEffect(() => {
  // 在頁面載入時發送 GET 請求
    async function fetchData() {
      try {
        const access_token = localStorage.getItem('access_token');
        // const refresh_token = localStorage.getItem('refresh_token');
        const response = await fetch("http://localhost:8000/reg/api/login", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${access_token}`,
          },
        });

        if (response.status === 200) {
          // 成功處理 GET 請求的回應
          const responseData = await response.json();
          router.push({
            pathname : responseData.redirect
          })
        } else {
          // 處理 GET 請求失敗的情況
          // const responseData = await response.json();
          if(response.status === 403){
            localStorage.clear('access_token');
            localStorage.clear('refresh_token');
          }
        }
      } catch (error) {
        // 處理 GET 請求時的錯誤
        console.error(error);
      }
    }

    fetchData(); // 執行 GET 請求

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // 空依賴項表示僅在組件載入時執行一次

// 按下送出按鈕後
const handleSubmit = async (e) => {
  e.preventDefault();
  
  // 驗證電子郵件地址格式
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailPattern.test(email)) {
    setErrorMessage("請輸入有效的電子郵件地址！");
    return;
  }

  // 清除錯誤消息
  setErrorMessage("");

  // 如果格式驗證通過，執行表單提交操作
  try {
    const response = await fetch("http://localhost:8000/reg/api/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.status === 200) {
      // 提交成功，執行你的成功操作
      const responceData = await response.json();
      console.log(responceData['resource'])
      router.push({
        pathname: "../uchi",
        // query: { resource: JSON.stringify(responceData['resource']) }, // 通過query参數傳遞數據
      });
      localStorage.setItem('access_token', responceData.access_token);
      localStorage.setItem('refresh_token', responceData.refresh_token);
    } else {
      // 提交失敗，處理錯誤情況
      // router.push("/error"); // 失敗後跳轉到 "/error" 頁面
      const errorData = await response.json();
      setErrorMessage(errorData.message); // 假設後端返回了一個包含錯誤消息的 JSON
      console.log(data)
    }
  } catch (error) {
    // 處理錯誤情況
    console.log(error)
  }

};
    
  return (
  <div>
    <Head>
      <title>登入</title>
      <meta name="register" content="使用者登入的頁面" />
    </Head>
    <h1>登入</h1>
    <form action="http://localhost:8000/reg/login" method="POST" onSubmit={handleSubmit}>
      <label htmlFor="email">Email:</label>
      <input
      type="text"
      id="email"
      name="email"
      required
      value={email}
      onChange={(e) => setEmail(e.target.value)}
      />
      <br />
      <label htmlFor="password">Password:</label>
      <input
      type="password"
      id="password"
      name="password"
      required
      value={password}
      onChange={(e) => setPassword(e.target.value)}
      />
      <br />
      <Link href={'./register'}>沒有帳號?</Link><Link href={'./forgetpassword'}>忘記密碼?</Link>
      <br />
      <button type="submit">點擊登入</button>
    </form>

    {errorMessage && <div style={{ color: "red" }}>{errorMessage}</div>}
  </div>
  );
}

// export async function getStaticProps() {
//     // Instead of the file system,
//     // fetch post data from an external API endpoint
//     const res = await fetch("http://localhost:8000/ifm/api/ifm");
//     const data = await res.json();
//     return {
//       props: {
//         data: data,
//         done: true,
//       }
//     }
// }