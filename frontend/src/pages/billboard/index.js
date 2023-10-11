import { useEffect, useReducer, useState } from "react";
import Head from "next/head";
import Link from "next/link";
import LoginState from "@/components/loginstate";
import style from "@/pages/billboard/css/index.module.css"
import { Router, useRouter } from "next/router";
import { redirect } from "next/dist/server/api-utils";


export default function Billboard(){
    const [title, setTitle] = useState({});
    const router = useRouter();
    const initialSetPage = async () =>{
        try {
            const response = await fetch("http://127.0.0.1:8000/billboard/api/gettitle/",{
                method:'GET',
            });

            if (response.status === 200){
                const responseData = await response.json();
                console.log(responseData);
                setTitle(responseData.title);
            } else {
                const responseData = await response.json();
                console.log(responseData);
            }
        } catch (error) {
            console.error(error)
        }

    }

    const divClick = (key) =>{
        router.push(`/billboard/${key}`);
    }
    const backpageClick = ()=>{
        router.push('./uchi');
    }
    useEffect(() => {
        initialSetPage();        
    }, []);
    
    return(
        <>  
            <Head><title>公告欄</title></Head>
            
            <LoginState
                profilePath="./ifm"
                resetPasswordPath="../reg/resetpassword"
                logoutPath="./"

            />

            <div className={style.billboardpagecontainer}>
                {Object.keys(title).map((key, index)=>(
                    <div key={`billboardcontainer_${index}`} className={style.Billboardlinkcontainer}
                    onClick={()=>divClick(key)}
                    >
                    
                        <Link key={`bill_link_${index}`} href={`./billboard/${key}`}>{title[key]}</Link>
                    
                    </div>
                ))}
                <button className={style.button} onClick={backpageClick}>回上一頁</button>
            </div>
            
        </>
    );
}