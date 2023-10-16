import Head from 'next/head';
import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import LoginState from '@/components/loginstate';
import style from '@/pages/reg/css/val.module.css'
export default function CountdownTimer() {
    const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const [countdown, setCountdown] = useState(5);
    const [message, setMessage] = useState("驗證中請稍等");
    const router = useRouter(); // 初始化 useRouter
    
    useEffect(() => {
        const countdownInterval = setInterval(() => {
        if (countdown > 0) {
            setCountdown(countdown - 1);
            setMessage(`驗證中請稍等 ${countdown} 秒`);
        } else {
            clearInterval(countdownInterval); // 停止倒數計時
            setMessage("發送POST請求中..."); // 更新訊息為發送POST請求中
            sendPostRequest(); // 執行POST請求
        }
        }, 1000);
        
            return () => {
            clearInterval(countdownInterval); // 在組件卸載時停止計時器
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [countdown]);

    const sendPostRequest = async () => {
        try {
            // 執行POST請求到指定的網址
            let validation_token = localStorage.getItem('validation_token');
            if (validation_token === null){
                console.log('沒有token');
                console.log(router.query);
                validation_token = router.query['valdation_token'];
                console.log(validation_token);
            }
            const response = await fetch(`${backedUrl}/reg/api/val`, {
                
                method: "POST",
                headers:{
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${validation_token}`,
                },
                // 添加需要的請求標頭和數據
            });

            if (response.status === 200) {
                // POST請求成功，執行你的成功操作
                setMessage("POST請求成功！");
            } else if(response.status === 201) {
                // 伺服器建立使用者鄉資訊並驗證完成
                const responseData = await response.json()
                setMessage(`驗證成功！${responseData.message}`);
                localStorage.setItem('access_token', response.access_token);
                localStorage.clear('access_token');
                router.push(responseData.redirect);
            } else if(response.status === 302) {
                // 已經驗證過，請求跳轉。
                const responseData = await response.json();
                localStorage.clear('validaton_token');
                router.push(responseData.redirect);
            } else if(response.status === 500) {
                // POST請求失敗，處理錯誤情況
                setMessage(`POST請求失敗！`);
                
            } else {
                // POST請求失敗，處理錯誤情況
                const responseData = await response.json();
                setMessage(`POST請求失敗！${responseData.message}`);
                // console.log(responseData.message)
            }
        } catch (error) {
        // 處理錯誤情況
            console.error(error);
        }
    };

    return (
        
        <div>
        <Head>
            <title>驗證頁面</title>
            <meta name="description" content="自動跳轉的驗證頁面" />
        </Head>
        {/* <LoginState
                 profilePath="../../ifm"
                 resetPasswordPath="./"
                 logoutPath=""
        /> */}
        <div className={style.valpagecontainer}>
            <div className={style.valformcontainer}>
                <div className={style.loader}></div>
                {<div><label>{message}</label></div>}
            </div>
        </div>
        

        </div>
    );
}
