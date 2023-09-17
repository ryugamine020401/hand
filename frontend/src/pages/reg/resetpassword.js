import LoginState from "@/components/loginstate";
import Head from "next/head";
import { useRouter } from "next/router";
import { useEffect } from "react";

export default function ResetPassword(){
    const router = useRouter();
    useEffect(()=>{
        const access_token = localStorage.getItem('access_token');
        if (access_token === null){
            router.push('../../uchi');
        }

    },[])


    return(
        
        <>
            <LoginState
                profilePath="../../ifm"
                resetPasswordPath="./resetpassword"
                logoutPath="../../uchi"
            />
            <Head><title>重設密碼</title></Head>
            <h1>重設密碼_登入後</h1>
        </>
    );
}