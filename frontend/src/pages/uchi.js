// import { useRouter } from "next/router";

import { useEffect } from "react";
import LoginState from "../components/loginstate"
import Head from "next/head";
import Link from "next/link";
import style from '@/pages/uchi.module.css'

export default function Home(){
    // const msg = useMsg(); // 直接使用 useMsg 函數獲取 msg 值
    // const router = useRouter();
    // resource是一個list
    // const resource = JSON.parse(router.query.resource || "{}"); // 解析數據
    const resource = ['佈告欄','線上聊天室', '討論區', '學習中心',  '個人資訊']
    const resourceObjext = {
        './billboard':'佈告欄', 
        './onlinechat':'線上聊天室', 
        './forum':'討論區', 
        './study':'學習中心', 
        './ifm':'個人資訊'}

    console.log('Data >>', {resource})
    return(
        <>
            <LoginState
                profilePath="./ifm"
                resetPasswordPath="./reg/resetpassword"
                logoutPath="./uchi"
            />
            
            <Head>
                <title>首頁</title>
            </Head>
            
            <div className = {style.uchipagecontainer}>
                
                {/* <div>
                    {resource.map((item, index) => (
                        <Link key={index} href=''>{item}</Link>
                    ))}
                </div> */}
                <div className={style.uppercontainer}>
                    {Object.keys(resourceObjext).slice(0,2).map((key, index) =>(  
                        <div key={`resourceupper_${index}`}>
                            <Link 
                            href={key} 
                            className={`link_${index}`} 
                            key={`uchi_resourcelink_${index}`}
                            >
                                {resourceObjext[key]}
                            </Link>
                        </div>
                    ))}
                </div>

                <div className={style.lowercontainer}>
                    {Object.keys(resourceObjext).slice(2,5).map((key, index) =>(  
                        <div key={`resourceupper_${index}`}>
                            <Link 
                            href={key} 
                            className={`link_${index}`} 
                            key={`uchi_resourcelink_${index}`}
                            >
                                {resourceObjext[key]}
                            </Link>
                        </div>
                    ))}
                </div>
            </div>
            
        </>
        
    );
}