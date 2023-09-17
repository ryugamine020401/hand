/*

  若沒有驗證過的帳號登入會自動跳出此頁面。

*/
import Head from "next/head";
import { useRouter } from "next/router";
import { useState, useEffect } from "react";

export default function Valemail({email}){
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
            const response = await fetch("http://127.0.0.1:8000/reg/api/valdatae", {
                method:"POST",
                body:JSON.stringify({ validationNum }),
                headers:{
                    'Content-Type' : 'application/json',
                    'Authorization': `Bearer ${access_token}`
                }
            });
            if( response.status === 200){
                const responseData = await response.json();
                console.log(responseData.message);
                router.push('./login');
                localStorage.clear('access_token');
                localStorage.clear('refresh_token');
            } else {
                const responseData = await response.json();
                console.log(responseData.message);
                setErrorMessage(responseData.message);
                if (response.status === 403){
                    localStorage.clear('access_token');
                    localStorage.clear('refresh_token');
                    router.push('./login')
                }
            }
        } catch (error) {
            console.log(error);
        }

    }


    const resendButtonClick = async () =>{
        const access_token = localStorage.getItem('access_token');
        setButtonEnable(false);
        setCountDown(60);
        try{
            
            const response = await fetch("http://127.0.0.1:8000/reg/api/emailresend", {
                method:"POST",
                body:JSON.stringify({email}),
                headers:{   
                    "Content-Type" : "application/json",
                    "Authorization": `Bearer ${access_token}`,
                }
            });

            if(response.status === 200){
                const responseData = await response.json();
                console.log(responseData.message);
                
            } else {
                const responseData = await response.json();
                console.log(responseData.message);
                if (response.status === 401) {
                    router.push('./login');
                }
                setErrorMessage(responseData.message);
            }

        } catch (error) {
            console.error(error);
        }
    }
    /* 
    useEffect(()=>{}, [XXX, XXX]);
    setInterval(()=>{}, <秒>);
     */
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
            <h1>驗證頁面</h1>
            <label>驗證碼</label>
            <input
                type="number"
                className="valdatioNum"
                onChange={(e) => setValidationNum(e.target.value)}
            />
            <button
                className="valdatebutton"
                onClick={sendValButtonClick}
            >
                點擊驗證
            </button>
            <br/>
            <label>沒有收到?</label>
            <button
                className="resendeemailbutton"
                onClick={resendButtonClick}
                disabled={!butonEnable}
            >
                再發送一次
            </button>
            {errorMessage && <span style={{ color:"red" }}>{errorMessage}</span>}
            {!butonEnable && <span>{message}</span>}


        
        
        </>
    );
}