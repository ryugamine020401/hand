import Head from "next/head";
import Image from "next/image";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/router"; // 導入 useRouter
import LoginState from "@/components/loginstate";
import style from "@/pages/reg/register.module.css"

export default function Register() {
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");   // 第一次密碼
    const [password_check, setPassword_Check] = useState("");   // 確認密碼
    const [passwordsLegth, setpasswordsLegth] = useState(false); // 用於檢查密碼長度
    const [passwordsMatch, setPasswordsMatch] = useState(false); // 用於檢查密碼匹配
	const [buttonClick, setButtonClick] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");
    const [birthday, setBirthday] = useState(""); 
    const router = useRouter(); // 初始化 useRouter


     // 在password和password_check改變時檢查密碼是否匹配
    const handlePasswordLegthCheckChange = (e) => {
        const confirmPassword = e.target.value;
        setPassword(confirmPassword);
        setPasswordsMatch(false)
        const isPasswordLegthEnought = confirmPassword.length >= 6;
        setpasswordsLegth(isPasswordLegthEnought);
		    const isPasswordMatch = confirmPassword === password_check && confirmPassword.length >= 6;
        setPasswordsMatch(isPasswordMatch);
        
    };

    // 在password和password_check改變時檢查密碼是否匹配
    const handlePasswordCheckChange = (e) => {
        const confirmPassword = e.target.value;
        setPassword_Check(confirmPassword);
        const isPasswordMatch = confirmPassword === password && confirmPassword.length >= 6;
        setPasswordsMatch(isPasswordMatch);
    };

  // 按下送出按鈕後
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!passwordsMatch) {
            setErrorMessage("密碼不符合要求！");
            return;
          }
        // 驗證電子郵件地址格式
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!emailPattern.test(email)) {
            setErrorMessage("請輸入有效的電子郵件地址！");
            return;
        }
        // 清除錯誤消息
        setErrorMessage("");
        // 如果格式驗證通過，執行表單提交操作
		setButtonClick(true);
        try {
        const response = await fetch("http://localhost:8000/reg/api/register", {
            method: "POST",
            body: JSON.stringify({ username, email, password, password_check, birthday }),
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
            const responceData = await response.json();
            setErrorMessage(responceData.message); // 假設後端返回了一個包含錯誤消息的 JSON
            // console.log(responceData.validaton_token)
            if (response.status === 201){
                // 建立成功，設定驗證token
                localStorage.setItem('validaton_token', responceData.validaton_token);
                localStorage.setItem('access_token', responceData.access_token);
                router.push('./valemail');
            }
        }
        } catch (error) {
        // 處理錯誤情況
        console.log(error)
        }

    };
 
  return (
    <div>
        <Head>
            <title>註冊</title>
            <meta name="register" content="使用者註冊的頁面" />
        </Head>
		<LoginState
            profilePath="../../ifm"
            resetPasswordPath="./"
            logoutPath=""
        />
      	<div className={style.registerpageconntainer}>
			<div className={style.registerformcontainer}>
				<div className="useramecotainer">
					<Image src="/images/username.png" width={20} height={20} alt="usernameicon"/>
					<label htmlFor="username">使用者暱稱:</label>
					<input
						type="text"
						id="username"
						name="username"
						required
						value={username}
						onChange={(e) => setUsername(e.target.value)}
						/>
				</div>
				<div className="emailcontainer">
				<Image src="/images/email.png" width={20} height={20} alt="usernameicon"/>
					<label htmlFor="email">電子郵件:</label>
					<input
					type="text"
					id="email" name="email"
					required
					value={email}
					onChange={(e) => setEmail(e.target.value)}
					/>
				</div>
				<div className="passwordcontainer">
				<Image src="/images/password.png" width={20} height={20} alt="usernameicon"/>
					<label htmlFor="email">密碼:</label>
					<input
					type="password"
					id="password" name="password"
					required
					value={password}
					onChange={handlePasswordLegthCheckChange}
					/>
					{passwordsLegth && <span style={{ color: "green" }} className={style.errormsg}> &#10003; </span>}
					{!(passwordsLegth) && <span style={{ color: "red" }} className={style.errormsg}> 密碼長度不足 </span>}
				</div>
				<div className="passwordcontainer">
				<Image src="/images/password.png" width={20} height={20} alt="usernameicon"/>
					<label htmlFor="password">確認密碼:</label>
					<input
					type="password"
					id="password_check" name="password_check"
					required
					value={password_check}
					onChange={handlePasswordCheckChange}
					/>
					{passwordsMatch && <span style={{ color: "green" }} className={style.errormsg}> &#10003; </span>}
					{!(passwordsMatch) && <span style={{ color: "red" }} className={style.errormsg}> 兩次輸入的密碼不相符 </span>}
					
				</div>
				
				<div className="birthdaycontainer">
					<Image src="/images/birthday.png" width={20} height={20} alt="usernameicon"/>
					<label htmlFor="birthday">生日:</label>
					<input
					type="date"
					id="birthday" name="birthday"
					required
					value={birthday}
					onChange={(e) => setBirthday(e.target.value)}
					/>
				</div>	
				<button type="submit" onClick={handleSubmit} className={style.button}>點擊註冊</button>
				{buttonClick && <div className={style.loader}/>}
				{errorMessage && <div style={{ color: "red" }}>{errorMessage}</div>}
				
			</div>
		</div>
    </div>
  );
}