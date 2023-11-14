import LoginState from "@/components/loginstate";
import Head from "next/head";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Image from "next/image";
import React, { useCallback } from 'react';
import style from '@/pages/ifm/css/card.module.css'
import WordCardStyle from '@/pages/study/css/SingLanguage.module.css';


function UserWordCard(){
    const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    // const [userWordcardURL, setUserWordcardURL] = useState([]);
    const [userWordcardURL2, setUserWordcardURL2] = useState({});
    
    const [wordCardData, setWordCardData] = useState({});
    const router = useRouter();
    const DeleteUserSignCardButtonCheck = async (vocabularie) =>{
        /* 刪除手語 */
        const access_token = localStorage.getItem('access_token');

        try {
            const response = await fetch(`${backedUrl}/ifm/api/getusersignlanguage`,{
                method:"DELETE",
                body:JSON.stringify(vocabularie),
                headers:{
                    'Authorization':`Bearer ${access_token}`,
                    'Content-Type':'application/json',
                }
            });
            if(response.status === 200){
                const responseData = await response.json();
                const newWordCardData = { ...wordCardData };
                delete newWordCardData[vocabularie];
                setWordCardData(newWordCardData);
                // console.log(responseData);
            } else if(response.status === 403) {
                localStorage.clear('access_token');
                localStorage.clear('refresh_token');
                alert('登入過期，請重新登入。');
                router.push('/reg/login');
            }else {
                const responseData = await response.json();
                // console.log(responseData);
            }
        } catch (error) {
            console.log(error);
        }
    }

    const DeleteUserWordCardButtonCheck = async (key) =>{
        const access_token = localStorage.getItem('access_token');

        try {
            const response = await fetch(`${backedUrl}/ifm/api/card`,{
                method:"DELETE",
                body:JSON.stringify(key),
                headers:{
                    'Authorization':`Bearer ${access_token}`,
                    'Content-Type':'application/json',
                }
            });
            if(response.status === 200){
                const responseData = await response.json();
                // router.reload();
                const newGestureCardData = {...userWordcardURL2};
                delete newGestureCardData[key];
                setUserWordcardURL2(newGestureCardData);
                // console.log(responseData);
            } else if(response.status === 403) {
                localStorage.clear('access_token');
                localStorage.clear('refresh_token');
                alert('登入過期，請重新登入。');
                router.push('/reg/login');
            }else {
                const responseData = await response.json();
                // console.log(responseData);
            }
        } catch (error) {
            // console.log(error);
        }
        // console.log(key);
    }

    const checkAcccesstoken = () => {
        const acccess_token = localStorage.getItem('access_token');
        if (acccess_token === null){
            router.push('../reg/login');
        }
    }



    const getWordcardInitial = async () => {
        const acccess_token = localStorage.getItem('access_token');
        try {
            const response = await fetch(`${backedUrl}/ifm/api/card`,{
                method:"GET",
                headers:{
                    'Authorization' : `Bearer ${acccess_token}`,
                    'Content-Type' : 'application/json',
                }
            });
            if (response.status === 200){
                const responseData = await response.json();
                setUserWordcardURL2(responseData.image_url_json);
                
            } else {
                const responseData = await response.json();
                // console.log(responseData.message);
            }
        } catch (error) {
            // console.log(error);
        }
    }
    useEffect(()=>{
        checkAcccesstoken();
        getWordcardInitial();
    }, [])

    /*---------------------- 獲得手語字卡 -------------------------------- */
    const getWordCard = async() => {
        const access_token = localStorage.getItem('access_token');
        if (access_token === null){
            router.push('/');
            return
        }
        const responst = await fetch(`${backedUrl}/ifm/api/getusersignlanguage`,{
            method:'GET',
            headers:{
                'Authorization' : `Bearer ${access_token}`,
                'Content-Type':'application/json',
            }
        });

        try {
            if (responst.status === 200) {
                const responseData = await responst.json();
                console.log(responseData.resource);
                setWordCardData(responseData.resource);

            } else {
                const responseData = responst.json();
                console.log(responseData);
            }
        } catch (error) {
            console.error(error);
        }

    }
    useEffect(()=>{
        getWordCard();
    },[])

    /*---------------------- 獲得手語字卡 -------------------------------- */
    return(
        <>
            <Head>
                <title>個人字卡</title>
            </Head>
            <LoginState
                profilePath="./"
                resetPasswordPath="../../reg/resetpassword"
                logoutPath="../../"
            />
            {/* <h1>字卡</h1> */}
            <div className={style.ifmcardpagecontainer}>
                <button className={style.repagebtn} onClick={()=>router.push('./')}>上一頁</button>
                <h1 className={style.pagetitle}> 使用者字卡 </h1>
                <div className={style.wordcardcontainer}>
                {Object.keys(userWordcardURL2).map((key, index) => (
                    <div key={`UserWordCardContainer_${index}`} className={style.wordcard}>
                        <div className={style.wordcardleft}>
                            <Image
                                priority
                                height={100}
                                width={100}
                                alt="字卡"
                                src={userWordcardURL2[key]}
                                key={`UserWordCardImage_${index}`}
                                />
                        </div>
                        <div className={style.wordcardright}>
                            <div className={style.describecontainer}>
                                <p key={`UserWordCardDescribe_${index}`}>字母手勢{key}</p>
                            </div>
                            <div className={style.buttoncontainer}>
                                <button key={`DeleteWordCardbutton_${index}`} onClick={() => DeleteUserWordCardButtonCheck(key)}>刪除字卡</button>
                            </div>
                        </div>
                    </div>
                ))}

                {Object.keys(wordCardData).map((key, index)=>(
                    <div key={`signlanguage_${index}`} className={WordCardStyle.cardcontainer}>
                        <div className={WordCardStyle.leftcardcontainer}>
                            <img src={wordCardData[key][2]}/>
                        </div>
                        <div className={WordCardStyle.rightcardcontainer}>
                            <div className={WordCardStyle.rCtopcontainer}>
                                <p>{key}</p>
                            </div>
                            <div className={WordCardStyle.rCdowncontainer}>
                                <a href={wordCardData[key][1]}>影片教學</a>
                                <p>{wordCardData[key][0]}</p>
                                
                                <button
                                onClick={() => DeleteUserSignCardButtonCheck(key)}
                                >刪除字卡</button>
                            </div>
                            
                        </div>
                    </div>
                ))}

                </div>
                <Image
                    width={400}
                    height={354}
                    alt="pic"
                    src={'/images/ifm_wordcadbook.png'}
                    className={style.leftpic}
                />
                <Image
                    width={400}
                    height={354}
                    alt="pic"
                    src={'/images/ifm_wordcadteacher.png'}
                    className={style.rightpic}
                />
            </div>
        </>
    );
}


export default UserWordCard;