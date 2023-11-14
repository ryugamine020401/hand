import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Head from "next/head";
import Link from "next/link";
import style from '@/pages/study/css/SingLanguage.module.css';
import LoginState from "@/components/loginstate";

export default function SignLanguage(){
    const router = useRouter();
    const [pageNum, setPageNum] = useState(1);
    const [wordCardData, setWordCardData] = useState({});
    const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const [loginButtonEnable, setLoginButtonEnable] = useState([]);
    const [enableCuttunClick, setEnableCuttunClick] = useState(false);

    const [chinese, setChinese] = useState();
    const [picurl, setPicurl] = useState();
    const [videourl, setVideourl] = useState();
    const [vocabularie, setVocabularie] = useState();

    
    /* -------------------------------- 初始設定 ---------------------------- */
    const getWordCard = async() => {
        const access_token = localStorage.getItem('access_token');
        if (access_token === null){
            setEnableCuttunClick(false);
        } else {
            setEnableCuttunClick(true);
        }
        const responst = await fetch(`${backedUrl}/study/api/getsignLanguage`,{
            method:'POST',
            body:JSON.stringify({pageNum}),
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

    const getButtonEnable = async() => {
        // signlanguagebtnCheck
        const access_token = localStorage.getItem('access_token');
        const responst = await fetch(`${backedUrl}/study/api/signlanguagebtnCheck`,{
            method:'GET',
            headers:{
                'Authorization' : `Bearer ${access_token}`,
                'Content-Type':'application/json',
            }
        });

        try {
            if (responst.status === 200) {
                const responseData = await responst.json();
                console.log(responseData.message);
                console.log(responseData.enablelist);
                setLoginButtonEnable(responseData.enablelist);
                // setWordCardData(responseData.message);


            } else {
                const responseData = responst.json();
                console.log(responseData.message);
            }
        } catch (error) {
            console.error(error);
        }
    } 
    useEffect(()=>{
        getWordCard();
        getButtonEnable();
    },[pageNum]);

    /* -------------------------------- 初始設定 ---------------------------- */
    /* ------------------ 換頁 --------------------- */
    const ChangePageUP = (num) =>{
        const cnt = num + 1 <= 5 ? num + 1:5;
        setPageNum(cnt);
    }
    const ChangePageDown = (num) =>{
        const cnt = num - 1 > 0 ? num - 1:1;
        setPageNum(cnt);
    }
    /* ------------------ 換頁 --------------------- */

    /* ---------------------- 加入字卡且刷新按鈕  --------------------- */
    const addSignLanguageCard = async(vocabularie, chinese, picurl, videourl) =>{
        
        setChinese(chinese);
        setPicurl(picurl);
        setVideourl(videourl);
        setVocabularie(vocabularie);
        
        const access_token = localStorage.getItem('access_token');
        
        const responst = await fetch(`${backedUrl}/study/api/addsignlanguagecard`,{
            method:'POST',
            body:JSON.stringify({chinese, vocabularie, picurl, videourl}),
            headers:{
                'Authorization' : `Bearer ${access_token}`,
                'Content-Type':'application/json',
            }
        });

        try {
            if (responst.status === 200) {
                const responseData = await responst.json();
                console.log(responseData.message);
                setLoginButtonEnable(prevState => [...prevState, vocabularie]);

            } else {
                const responseData = responst.json();
                console.log(responseData);
            }
        } catch (error) {
            console.error(error);
        }
    }

    // useEffect(()=>{
    //     getButtonEnable();
    // },[loginButtonEnable]);
    /* ---------------------- 加入字卡且刷新按鈕  --------------------- */

    return(
        <>
            <div className={style.pagecontainer}>
                <Head><title>學習資源</title></Head>
                <LoginState
                        profilePath="../ifm"
                        resetPasswordPath="./reg/resetpassword"
                        logoutPath="../uchi"
                />
                
                <div className={style.ALLcardcontainer}>
                    {Object.keys(wordCardData).map((key, index)=>(
                        <div key={`signlanguage_${index}`} className={style.cardcontainer}>
                            <div className={style.leftcardcontainer}>
                                <img src={wordCardData[key][2]}/>
                            </div>
                            <div className={style.rightcardcontainer}>
                                <div className={style.rCtopcontainer}>
                                    <p>{key}</p>
                                </div>
                                <div className={style.rCdowncontainer}>
                                    <a href={wordCardData[key][1]}>影片教學</a>
                                    <p>{wordCardData[key][0]}</p>

                                    {/* <button onClick={()=>addSignLanguageCard(
                                        key, wordCardData[key][0], wordCardData[key][2], wordCardData[key][1]
                                    )}>加入字卡</button> */}

                                    {enableCuttunClick ? (
                                        loginButtonEnable.includes(key) ? (
                                            <button disabled={true}
                                                className={style.noneloginbutton}
                                                
                                            >已加入</button>
                                        ):(
                                            <button onClick={()=>addSignLanguageCard(
                                                key, wordCardData[key][0], wordCardData[key][2], wordCardData[key][1]
                                            )}>加入字卡</button>
                                        )
                                    ):(
                                        <button disabled={true} className={style.noneloginbutton}>請先登入</button>
                                    )}


                                    {/* vocabularie, chinese, picurl, videourl */}
                                </div>
                                
                            </div>
                        </div>
                    ))}
                </div>
                <div className={style.changepagecontainer}>
                    <button onClick={()=>ChangePageDown(pageNum)} className={style.button}>上一頁</button>
                    <p className={style.pagenumber}>{pageNum}</p>
                    <button onClick={()=>ChangePageUP(pageNum)} className={style.button}>下一頁</button>
                </div>
                
            </div>
        </>
    )
}