// import { useRouter } from "next/router";
import { useEffect } from "react";
import LoginState from "../components/loginstate"
import Head from "next/head";

export default function Home(){
    // const msg = useMsg(); // 直接使用 useMsg 函數獲取 msg 值
    // const router = useRouter();
    // resource是一個list
    // const resource = JSON.parse(router.query.resource || "{}"); // 解析數據
    const resource = ['佈告欄', '討論區', '學習中心', '線上聊天室', '個人資訊']
    

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
                <div>
                    {resource.map((item, index) => (
                        <button key={index}>{item}</button>
                    ))}
                </div>
            </section>
        </div>
        
    );
}