import LoginState from "@/components/loginstate";
import Head from "next/head";
import Image from "next/image";
import { useEffect, useState } from "react";
import style from '@/pages/study/css/english.module.css'
import { useRouter } from "next/router";

export default function Studyindex() {
    const nginxdomain = process.env.NEXT_PUBLIC_NGINX_DOMAIN;
    const [englishWordCard, setEnglishWordCard] = useState({});
    const [loginButtonEnable, setLoginButtonEnable] = useState([]);   // 以加入的字卡不能再點擊加入
    const [enableCuttunClick, setEnableCuttunClick] = useState(false);
    const router = useRouter();
    const initialChecking = async () => {
        const nginxdomain = process.env.NEXT_PUBLIC_NGINX_DOMAIN;
        const acccess_token = localStorage.getItem('access_token');
        if (acccess_token === null){
            setEnableCuttunClick(false);
        }else{
            setEnableCuttunClick(true);
        }
        try {
            const response = await fetch(`${nginxdomain}/study/api/english`,{
                method:'GET',
                headers:{
                    'Authorization':`Bearer ${acccess_token}`,
                }
            });
            if (response.status === 200){
                const responseData = await response.json();
                // console.log(responseData);
                setEnglishWordCard(responseData.wordcard);
                // console.log(responseData.wordcard);
            } else {
                const responseData = await response.json();
                console.log(responseData);
                setEnglishWordCard(responseData.wordcard);
            }

        } catch (error) {
            console.log(error);
        }
    }

    const addUserWordCardButtonClick = async(key) =>{
        console.log(key);
        const access_token = localStorage.getItem('access_token');
        try {
            const response = await fetch(`${nginxdomain}/study/api/english`, {
                method:'POST',
                body:JSON.stringify(key),
                headers:{
                    'Authorization' : `Bearer ${access_token}`,
                    'Content-Type':'application/json',
                }
            });
            if (response.status === 200) {
                const responseData = await response.json();
                console.log(responseData);
                buttonenablecheck();
            } else if(response.status === 403){
                alert('登入狀態過期。')
                // 要求加入字卡但token過期
                setEnableCuttunClick(false);
            } else if(response.status === 401){
                // 要求加入字卡但沒有token
                alert('登入後才能執行此操作。')
                setEnableCuttunClick(false);
            } else {
                const responseData = await response.json();
                console.log(responseData);
            }
        } catch (error) {
            console.error(error)
        }
    }

    const buttonenablecheck = async() =>{
        // 登入後檢測使用者哪個字卡已經加入，哪個沒有加入。

        const access_token = localStorage.getItem('access_token');
        try {
            const response = await fetch(`${nginxdomain}/study/api/wordcardbuttoncheck`,{
                method:"GET",
                headers:{
                    'Authorization':`Bearer ${access_token}`,
                }

            });
            if (response.status === 200) {
                const responseData = await response.json();
                console.log(responseData);
                setLoginButtonEnable(responseData.enablelist);
            } else {
                const responseData = await response.json();
                console.log(responseData);
            }
        } catch (error) {
            console.error(error);
        }
    }

    useEffect(() => {
        initialChecking();
        buttonenablecheck();
    }, [])

    return(
    
        <>
            <Head><title>英文字母手勢</title></Head>
            <LoginState
                profilePath="../ifm"
                resetPasswordPath="./reg/resetpassword"
                logoutPath="./uchi"
            />
            <div className={style.englishpagecontainer}>
                <button className={style.repagebtn} onClick={()=>router.push('./ ')}>上一頁</button>
                <div className={style.wordcardcontainer}>
                    {Object.keys(englishWordCard).map((key, index)=>(
                    <div key={`wordcardImage_cotainer_${index}`} className={style.alphabetcontainer}>
                            <Image
                                priority
                                className={`word_alphabet_image_${index}`} 
                                key={`study_english_image_${index}`} 
                                src={englishWordCard[key]}
                                width={150}
                                height={150}
                                alt={'手勢圖片'}
                                style={{'margin': 30}}
                            />
                            {enableCuttunClick ?(
                                
                                loginButtonEnable.includes(index) ?(
                                    
                                    <button 
                                        disabled={enableCuttunClick}
                                        
                                        id= {index}
                                        key={`addUserword_card_btn_${index}`} 
                                        onClick={()=>addUserWordCardButtonClick(key)}
                                    >已加入</button>
                                ):(
                                    <button 
                                        disabled={!enableCuttunClick} 
                                        id= {index}
                                        key={`addUserword_card_btn_${index}`} 
                                        onClick={()=>addUserWordCardButtonClick(key)}
                                    >加入字卡</button>
                                )
                            )
                            :
                            (
                                <button 
                                disabled={!enableCuttunClick} 
                                key={`addUserword_card_btn_${index}`} 
                                onClick={()=>addUserWordCardButtonClick(key)}
                                >請先登入</button>

                            )}
                            
                        </div>
                    ))}
                </div>
            </div>
        </>
    );

}