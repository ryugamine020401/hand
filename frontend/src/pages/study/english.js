import LoginState from "@/components/loginstate";
import Head from "next/head";
import Image from "next/image";
import { useEffect, useState } from "react";

export default function Studyindex() {
    const [englishWordCard, setEnglishWordCard] = useState({});
    const [userWordcardId, setUserWordcardId] = useState();
    const initialChecking = async () => {
        const acccess_token = localStorage.getItem('access_token');

        try {
            const response = await fetch("http://127.0.0.1:8000/study/english",{
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
            const response = await fetch("http://127.0.0.1:8000/study/english", {
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
            } else {
                const responseData = await response.json();
                console.log(responseData);
            }
        } catch (error) {
            console.error(error)
        }
    }

    useEffect(() => {
        initialChecking();
    }, [])

    return(
    
        <>
            <Head><title>英文字母手勢</title></Head>
            <LoginState
                profilePath="../ifm"
                resetPasswordPath="./reg/resetpassword"
                logoutPath="./uchi"
            />
            {Object.keys(englishWordCard).map((key, index)=>(
               <div key={`wordcardImage_cotainer_${index}`}>
                    <Image
                        priority
                        className={`word_alphabet_image_${index}`} 
                        key={`study_english_image_${index}`} 
                        src={englishWordCard[key]}
                        width={100}
                        height={100}
                        alt={'手勢圖片'}
                        style={{'margin': 30}}
                    />
                    <button key={`addUserword_card_btn_${index}`} onClick={()=>addUserWordCardButtonClick(key)}>加入字卡</button>
                </div>
            ))}
        </>
    );

}