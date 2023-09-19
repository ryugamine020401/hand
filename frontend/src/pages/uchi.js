// import { useRouter } from "next/router";

import { useEffect } from "react";
import LoginState from "../components/loginstate"
import Head from "next/head";
import Link from "next/link";

export default function Home(){
    // const msg = useMsg(); // 直接使用 useMsg 函數獲取 msg 值
    // const router = useRouter();
    // resource是一個list
    // const resource = JSON.parse(router.query.resource || "{}"); // 解析數據
    const resource = ['佈告欄', '討論區', '學習中心', '線上聊天室', '個人資訊']
    const resourceObjext = {
        './billnoard':'佈告欄', 
        './discuss':'討論區', 
        './study':'學習中心', 
        './onlinechat':'線上聊天室', 
        './ifm':'個人資訊'}

    console.log('Data >>', {resource})
    return(
        <div>
            <Head>
                <title>首頁</title>
            </Head>
            <LoginState
                profilePath="./ifm"
                resetPasswordPath="./reg/resetpassword"
                logoutPath="./uchi"
            />
            <section className = "fullscreen">
                <div><h1>Home</h1></div>
                {/* <div>
                    {resource.map((item, index) => (
                        <Link key={index} href=''>{item}</Link>
                    ))}
                </div> */}
                <div>
                    {Object.keys(resourceObjext).map((key, index) =>(
                        <>
                            <Link href={key} className={`link_${index}`} key={`uchi_resourcelink_${index}`}>{resourceObjext[key]}</Link>
                        </>
                    ))}
                </div>
            </section>
        </div>
        
    );
}