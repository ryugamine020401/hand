import LoginState from "@/components/loginstate";
import Head from "next/head";
import Image from "next/image";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import style from '@/pages/reg/css/resetpassword.module.css'

export default function ResetPassword(){
    const nginxdomain = process.env.NEXT_PUBLIC_NGINX_DOMAIN;
    const router = useRouter();
    const [password_old, setPassword_Old] = useState("");   // 舊密碼
    const [password_new, setPassword_New] = useState("");   // 新密碼

    const [password_check, setPassword_Check] = useState("");   // 確認密碼
    const [passwordsLegth, setpasswordsLegth] = useState(false); // 用於檢查密碼長度
    const [passwordsMatch, setPasswordsMatch] = useState(false); // 用於檢查密碼匹配

    const [errorMessage, setErrorMessage] = useState("");

    useEffect(()=>{
        const access_token = localStorage.getItem('access_token');
        if (access_token === null){
            router.push('../../uchi');
        }

    }, [])


     // 在password和password_check改變時檢查密碼是否匹配
    const handlePasswordLegthCheckChange = (e) => {
        const confirmPassword = e.target.value;
        setPassword_New(confirmPassword);
        setPasswordsMatch(false)
        const isPasswordLegthEnought = confirmPassword.length >= 6;
        setpasswordsLegth(isPasswordLegthEnought);
		const isPasswordMatch = confirmPassword === password_check && confirmPassword.length >= 6;
        setPasswordsMatch(isPasswordMatch);
        // setErrorMessage("密碼長度不足。");
        
    };

    // 在password和password_check改變時檢查密碼是否匹配
    const handlePasswordCheckChange = (e) => {
        const confirmPassword = e.target.value;
        setPassword_Check(confirmPassword);
        const isPasswordMatch = confirmPassword === password_new && confirmPassword.length >= 6;
        setPasswordsMatch(isPasswordMatch);
        // setErrorMessage("兩次輸入密碼不相同。");
    };

    const ResetPasswordClick = async () => {

        const access_token = localStorage.getItem('access_token');
        if (!passwordsMatch){
            return;
        } else {
            setErrorMessage("");
        }
        try {
            const response = await fetch(`${nginxdomain}/reg/api/repassword`, {
                method: 'POST',
                body : JSON.stringify({password_old, password_new}),
                headers:{
                    'Content-Type' : 'application/json',
                    'Authorization': `Bearer ${access_token}`
                }
                
            });

            if (response.status === 200){
                const responceData = await response.json();
                localStorage.clear('access_token');
                localStorage.clear('refresh_token');
                router.push('./login')
                console.log(responceData);
            } else {
                const responceData = await response.json();
                console.log(responceData);
                setErrorMessage(responceData.message);
            }
        } catch (error) {
            console.log(error)
        }
    }
    return(
        
        <>
            <LoginState
                profilePath="../../ifm"
                resetPasswordPath="./resetpassword"
                logoutPath="../../uchi"
            />
            <Head><title>重設密碼</title></Head>
            <div className={style.resetpwdpageconntainer}>
                <div className={style.resetpwdformcontainer}>
                <div className="pwdcontianer">
                <Image src="/images/oldpassword.png" width={20} height={20} alt="pwdicon"/>
                    <label htmlFor="password">舊密碼:</label>
                    <input
                    type="password"
                    id="password_check" name="password_check"
                    required
                    onChange={(e) => setPassword_Old(e.target.value)}
                    value={password_old}
                    />
                </div>
                <div className="newpwncontainer">
                    <Image src="/images/password.png" width={20} height={20} alt="pwdicon"/>
                    <label htmlFor="email">密碼:</label>
                    <input
                    type="password"
                    id="password" name="password"
                    required
                    value={password_new}
                    onChange={handlePasswordLegthCheckChange}
                    />
                    {passwordsLegth && <span style={{ color: "green" }} className={style.errormsg}> &#10003; </span>}
                    {!(passwordsLegth) && <span style={{ color: "red" }} className={style.errormsg}> 密碼長度不足 </span>}
                </div>
                
                <div className="pwncheckcontainer">
                    <Image src="/images/password.png" width={20} height={20} alt="pwdicon"/>
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
                

                <button
                    className={style.button}
                    onClick={ResetPasswordClick}
                >
                    修改密碼
                </button>
                <div>
                    {errorMessage && <p style={{color : 'red'}}>{errorMessage}</p>}
                </div>
                
                </div>
            </div>
            
            
            
            
            
            
        </>
    );
}