// import { useRouter } from "next/router";

import { useEffect, useState } from "react";
import LoginState from "../components/loginstate"
import Head from "next/head";
import Image from "next/image";
import Link from "next/link";
import style from '@/pages/uchi.module.css'
import { useRouter } from "next/router";

export default function Home(){
    // const msg = useMsg(); // 直接使用 useMsg 函數獲取 msg 值
    // const router = useRouter();
    // resource是一個list
    // const resource = JSON.parse(router.query.resource || "{}"); // 解析數據
    const router = useRouter();
    const [loginCheck, setLoginCheck] = useState(false);
    const resource = ['佈告欄','線上聊天室', '討論區', '學習中心',  '個人資訊']
    const UpperContainerImageSrc = [
        '/images/uchi_billboard.png', 
        '/images/uchi_onlinechat.png',
    ]
    const UpperImgClasslist = [style.billboardcontainer, style.onlinechatcontainer];
    const UppperContainerURL = [
        './billboard',
        './onlinechat'
    ]
    const LowerContainerImageSrc = [
        '/images/uchi_discuss.png', 
        '/images/uchi_study.png',
        '/images/uchi_information.png',
    ]
    const LowerImgClasslist = [style.discusscontainer, style.studycontainer, style.informationcontainer];
    const LowerImgClasslistnoLogin = [style.discusscontainer, style.studycontainer, style.informationcontainernologin];
    const lockClass = [style.discusslock, style.studylock, style.informationlock];
    const LowerContainerURL = [
        './forum',
        './study',
        './ifm',
    ]
    const resourceObjext = {
        './billboard':'佈告欄', 
        './onlinechat':'線上聊天室', 
        './forum':'討論區', 
        './study':'學習中心', 
        './ifm':'個人資訊'}
    
    // console.log('Data >>', {resource})

    const redirectDivClick = (url) =>{
        router.push(url);
        console.log(url);
    }
    useEffect(()=>{
        const access_token = localStorage.getItem('access_token');
        if (access_token === null) {
            console.log('沒登入');
        } else {
            console.log('有登入');
            setLoginCheck(true);
        }

    });
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
                        <div key={`resourceupper_${index}`} className={`${UpperImgClasslist[index]}`}
                            onClick={()=>redirectDivClick(UppperContainerURL[index])}
                        >
                            <Image
                            height={100}
                            width={100}
                            src={UpperContainerImageSrc[index]}
                            alt="上容器圖"
                            />
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
                        loginCheck?
                        (
                        <div key={`resourceupper_${index}`} className={`${LowerImgClasslist[index]}`}
                            onClick={()=>redirectDivClick(LowerContainerURL[index])}
                        >
                            <Image
                            height={100}
                            width={100}
                            src={LowerContainerImageSrc[index]}
                            alt="下容器圖"
                            />
                            <Link 
                            href={key} 
                            className={`link_${index}`} 
                            key={`uchi_resourcelink_${index}`}
                            >
                                {resourceObjext[key]}
                            </Link>
                        </div>
                        ):(
                        <div key={`resourceupper_${index}`} className={`${LowerImgClasslistnoLogin[index]}`}
                            onClick={()=>redirectDivClick(LowerContainerURL[index])}
                        >
                            <Image
                            height={100}
                            width={100}
                            src={'/images/uchi_lock.png'}
                            alt="下容器圖鎖"
                            className={`${lockClass[index]}`}
                            id={index}
                            />
                            <Image
                            height={100}
                            width={100}
                            src={LowerContainerImageSrc[index]}
                            alt="下容器圖"
                            />
                            <Link 
                            href={key} 
                            className={`link_${index}`} 
                            key={`uchi_resourcelink_${index}`}
                            >
                                {resourceObjext[key]}
                            </Link>
                        </div>
                        )
                    ))}
                </div>
            </div>
            
        </>
        
    );
}