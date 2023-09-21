import LoginState from "@/components/loginstate";
import Head from "next/head";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Image from "next/image";
import React, { useCallback } from 'react';


function UserWordCard(){
    // const [userWordcardURL, setUserWordcardURL] = useState([]);
    const [userWordcardURL2, setUserWordcardURL2] = useState({});
    const router = useRouter();

    const DeleteUserWordCardButtonCheck = async (key) =>{
        const access_token = localStorage.getItem('access_token');

        try {
            const response = await fetch("http://127.0.0.1:8000/ifm/api/card",{
                method:"DELETE",
                body:JSON.stringify(key),
                headers:{
                    'Authorization':`Bearer ${access_token}`,
                    'Content-Type':'application/json',
                }
            });
            if(response.status === 200){
                const responseData = await response.json();
                router.reload();
                console.log(responseData);
            } else {
                const responseData = await response.json();
                console.log(responseData);
            }
        } catch (error) {
            console.log(error);
        }
        console.log(key);
        

    }

    const checkAcccesstoken = useCallback(() => {
        const acccess_token = localStorage.getItem('access_token');
        if (acccess_token === null){
            // router.push('../');
        }
    }, [])



    const getWordcardInitial = async () => {
        const acccess_token = localStorage.getItem('access_token');
        try {
            const response = await fetch("http://127.0.0.1:8000/ifm/api/card",{
                method:"GET",
                headers:{
                    'Authorization' : `Bearer ${acccess_token}`,
                    'Content-Type' : 'application/json',
                }
            });
            if (response.status === 200){
                const responseData = await response.json();
                console.log(responseData);
                console.log(responseData.image_url_array);
                console.log(responseData.image_url_json);
                // setUserWordcardURL(responseData.image_url_array);
                setUserWordcardURL2(responseData.image_url_json);
                
            } else {
                const responseData = await response.json();
                console.log(responseData.message);
            }
        } catch (error) {
            console.log(error);
        }
    }
    useEffect(()=>{
        // checkAcccesstoken();
        getWordcardInitial();
        // let isMounted = true;

        // const fetchData = async () => {
        //     // 非同步操作
        //     if (isMounted) {
        //         // 確保元件仍然掛載
        //         await getWordcardInitial();
        //         await console.log(userWordcardURL2);
        //     }
        // };

        // fetchData();

        // return () => {
        //     isMounted = false;
        //     // 在元件卸載時取消非同步操作
        // };
        }, [])

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
            <h1>字卡</h1>

            {/* <div>
                {userWordcardURL ? (
                    userWordcardURL.map((url, index) => (
                    <div key={index} style={{'border':'3px solid red',margin:"5px"}}>
                        <Image
                          priority
                          height={50}
                          width={50}
                          alt="字卡"
                          src={url}
                        />
                        <p>這是描述圖像的文字</p>
                        <button key={index}>刪除字卡</button>
                      </div>
                    ))
                ) : (
                    <p>Loading...</p>
                )}
            </div> */}

            {Object.keys(userWordcardURL2).map((key, index) => (
                <div key={`UserWordCardContainer_${index}`} style={{'border':'3px solid red',margin:"5px"}}>
                    <Image
                          priority
                          height={50}
                          width={50}
                          alt="字卡"
                          src={userWordcardURL2[key]}
                          key={`UserWordCardImage_${index}`}
                        />
                    <p key={`UserWordCardDescribe_${index}`}>字母手勢{key}</p>
                    <button key={`DeleteWordCardbutton_${index}`} onClick={() => DeleteUserWordCardButtonCheck(key)}>刪除字卡</button>
                    {/* <p>{key}: {userWordcardURL2[key]}</p> */}
                    
                </div>
            ))}
            
        </>
    );
}


export default UserWordCard;