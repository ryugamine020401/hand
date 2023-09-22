import LoginState from "@/components/loginstate";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";



export default function SendBillboard() {
    const [content, setContent] = useState('');
    const [title, setTitle] = useState('');
    const router = useRouter();
    const CheckAccessToken = async() => {
        try {
            const access_token = await localStorage.getItem('access_token');
            const response = await fetch("http://127.0.0.1:8000/billboard/api/rootcheck",{
                method:'POST',
                headers:{
                    'Authorization':`Bearer ${access_token}`,
                }

            });
            if (response.status === 200) {
                const responseData = await response.json();
                console.log(responseData);
            } else {
                const responseData = await response.json();
                console.log(responseData);
                router.push('../uchi')
            }
        } catch (error) {
            console.log(error);
        }
    }

    const sendContentBunttonClick = async () => {
        
        try {
            const access_token = localStorage.getItem('access_token');
            if (!content.trim() || !title.trim()) {
                console.log('不能發送空白的公告.');
                return;
            }
            const response = await fetch("http://127.0.0.1:8000/billboard/api/send",{
                method:'POST',
                body:JSON.stringify({content, title}),
                headers:{
                    'Authorization':`Bearer ${access_token}`,
                    'Content-Type':'application/json',
                }
            });
            if (response.status === 200) {
                const responseData = await response.json();
                console.log(responseData);
                
            } else {
                const responseData = await response.json();
                console.log(responseData);
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
        <LoginState
            profilePath="../ifm"
            resetPasswordPath="../reg/resetassword"
            logoutPath="../uchi"
        />
        <h1>發送公告頁面</h1>
        <label>公告標題</label>
        
        <input
            type="text"
            onChange={(e)=>setTitle(e.target.value)}
        />
        <br/>
        <label>公告內容</label>
        <textarea
            rows="4" 
            cols="50"
            onChange={(e)=>setContent(e.target.value)}
        />
        <button onClick={sendContentBunttonClick}>送出公告</button>
        
    
    </>);
} 