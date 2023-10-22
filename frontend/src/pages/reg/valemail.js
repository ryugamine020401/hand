/*

  若沒有驗證過的帳號登入會自動跳出此頁面。

*/
import LoginState from "@/components/loginstate";
import Head from "next/head";
import Image from "next/image";
import { useRouter } from "next/router";
import { useState, useEffect } from "react";
import style from '@/pages/reg/css/valemail.module.css'

export default function Valemail({email}){
    const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const router = useRouter();
    const [errorMessage, setErrorMessage] = useState("");
    const [message, setMessage] = useState("");
    const [butonEnable, setButtonEnable] = useState(true);
    const [countdown ,setCountDown] = useState(0);
    const [validationNum, setValidationNum] =useState("");
    
    

    const sendValButtonClick = async () => {
        const validation_numPattern = /^\d{5,6}$/;
        if(validation_numPattern.test(validationNum)){
            setErrorMessage("");
        } else {
            setErrorMessage("請輸入6位數的驗證碼。");
            return;
        }

        try{
            const access_token = localStorage.getItem('access_token');
            const response = await fetch(`${backedUrl}/reg/api/valdatae`, {
                method:"POST",
                body:JSON.stringify({ validationNum }),
                headers:{
                    'Content-Type' : 'application/json',
                    'Authorization': `Bearer ${access_token}`
                }
            });
            if( response.status === 200){
                const responseData = await response.json();
                // console.log(responseData.message);
                router.push('../uchi');
                // localStorage.clear('access_token');
                // localStorage.clear('refresh_token');
            } else {
                const responseData = await response.json();
                // console.log(responseData.message);
                setErrorMessage(responseData.message);
                if (response.status === 403){
                    localStorage.clear('access_token');
                    localStorage.clear('refresh_token');
                    router.push('./login');
                }
            }
        } catch (error) {
            // console.log(error);
        }

    }


    const resendButtonClick = async () =>{
        setErrorMessage('');
        const access_token = localStorage.getItem('access_token');
        setButtonEnable(false);
        setCountDown(60);
        try{
            
            const response = await fetch(`${backedUrl}/reg/api/emailresend`, {
                method:"POST",
                body:JSON.stringify({email}),
                headers:{   
                    "Content-Type" : "application/json",
                    "Authorization": `Bearer ${access_token}`,
                }
            });

            if(response.status === 200){
                const responseData = await response.json();
                // console.log(responseData.message);
                
            } else {
                const responseData = await response.json();
                // console.log(responseData.message);
                if (response.status === 401) {
                    router.push('./login');
                }
                setErrorMessage(responseData.message);
            }

        } catch (error) {
            console.error(error);
        }
    }

    useEffect(()=>{
        let countdownInteval;
        const acccess_token_check = localStorage.getItem('access_token');
        if(countdown > 0 && butonEnable === false){
            countdownInteval = setInterval(()=>{
                setCountDown(countdown - 1);
                setMessage(`您還有 ${countdown - 1} 秒可以重新寄送郵件。`);
                
            }, 1000);
        } else {
            clearInterval(countdownInteval);
            if(acccess_token_check === null){
                router.push('./login')
            }
            setCountDown(60);
            setButtonEnable(true);
            setMessage(`您還有 ${countdown} 秒可以重新寄送郵件。`);
        }

        return () => {
            clearInterval(countdownInteval);
        };
    }, [countdown, butonEnable])

    return(
        <>
            <Head>
                <title>驗證信箱</title>
            </Head>
            <LoginState
                 profilePath="../../ifm"
                 resetPasswordPath="./"
                 logoutPath=""
            />
            <div className={style.valemailpagecontainer}>
                <div className={style.valemailformcontainer}>
                    <div className="valnumcontainer">
                    <Image src="/images/valdation.png" width={20} height={20} alt="valicon"/>
                        <label>驗證碼</label>
                        <input
                            type="number"
                            className="valdatioNum"
                            onChange={(e) => setValidationNum(e.target.value)}
                        />
                    </div>
                    {!butonEnable && <div style={{ color:"red" }}>{message}</div>}
                    {errorMessage && <div style={{ color:"red" }}>{errorMessage}</div>}
                    <button
                    className={style.button}
                    onClick={sendValButtonClick}>
                        點擊驗證
                    </button>
                    <div className={style.resendemaincontainer}>
                    <Image src="/images/resendmail.png" width={20} height={20} alt="valicon"/>
                        <label>沒有收到?</label>
                        <button
                            className="resendeemailbutton"
                            onClick={resendButtonClick}
                            disabled={!butonEnable}
                        >
                            再發送一次
                        </button>
                    </div>
                
                    
                    
                
                </div>
            </div>
            
            
            
            
            


        
        
        </>
    );
}