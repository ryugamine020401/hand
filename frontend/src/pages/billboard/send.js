import LoginState from "@/components/loginstate";
import Head from "next/head";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import style from '@/pages/billboard/css/send.module.css'


export default function SendBillboard() {
    const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const [content, setContent] = useState('');
    const [title, setTitle] = useState('');
    const router = useRouter();
    const CheckAccessToken = async() => {
        try {
            const access_token = await localStorage.getItem('access_token');
            const response = await fetch(`${backedUrl}/billboard/api/rootcheck`,{
                method:'POST',
                headers:{
                    'Authorization':`Bearer ${access_token}`,
                }

            });
            if (response.status === 200) {
                const responseData = await response.json();
                // console.log(responseData);
            } else {
                const responseData = await response.json();
                // console.log(responseData);
                router.push('../uchi')
            }
        } catch (error) {
            // console.log(error);
        }
    }

    const sendContentBunttonClick = async () => {
        
        try {
            const access_token = localStorage.getItem('access_token');
            if (!content.trim() || !title.trim()) {
                // console.log('不能發送空白的公告.');
                return;
            }
            const response = await fetch(`${backedUrl}/billboard/api/send`,{
                method:'POST',
                body:JSON.stringify({content, title}),
                headers:{
                    'Authorization':`Bearer ${access_token}`,
                    'Content-Type':'application/json',
                }
            });
            if (response.status === 200) {
                const responseData = await response.json();
                // console.log(responseData);
                router.push('./');
                
            } else {
                const responseData = await response.json();
                // console.log(responseData);
            }
        } catch (error) {
            console.error(error);
        }
    }

    useEffect(()=>{
        CheckAccessToken();
    },[])


    return(
    
    <>
    <Head><title>發送公告</title></Head>
        <LoginState
            profilePath="../ifm"
            resetPasswordPath="../../reg/resetpassword"
            logoutPath="/uchi"
        />
        <div className={style.pagecomstainer}>
            <div className={style.formcontainer}>
                <input
                    type="text"
                    onChange={(e)=>setTitle(e.target.value)}
                    placeholder="公告標題"
                />
                <textarea
                    rows="4" 
                    cols="50"
                    onChange={(e)=>setContent(e.target.value)}
                    placeholder="公告內容"
                />
                <button onClick={sendContentBunttonClick}>送出公告</button>
            </div>
        </div>
        
    </>);
} 