import Image from 'next/image';
import { useState, useEffect } from 'react';



export default function LoginState() {
    const [logincheck, setLogincheck] = useState(false);
    const [headimgurl, setHeadImgURL] = useState(false)
    const [buttommsg, setButtommsg] = useState("")
    const sendPostRequest = async () => {     
        try{
            const access_token = localStorage.getItem('access_token');
            const response = await fetch("http://127.0.0.1:8000/reg/api/logincheck",{

                method: "POST",
                headers:{
                    "Content-Type": "application/json",
                    "Authorization": `Beaer ${access_token}`,
                },
            });
            if (response.status === 202){
                // 驗證成功，具有登入狀態。
                const responseData = await response.json();
                console.log(responseData.loginstatus);
                console.log(responseData.headimgurl);
                setLogincheck(responseData.loginstatus);
                setButtommsg(responseData.buttom_word);
                setHeadImgURL(responseData.headimgurl)
            } else {
                // 驗證失敗，無登入狀態或過期。
                const responseData = await response.json();
                if ( response.status === 403){
                    console.log(responseData.detail)
                } else{
                    console.log(responseData.message)
                }
                setLogincheck(responseData.loginstatus);
                setButtommsg(responseData.buttom_word);
                
                
            }
        } catch(error) {
            console.log('有錯')
            console.log(error);
        }

    };

    useEffect(()=>{
        sendPostRequest();
    }, [])
    
    return(

        <div>
            {logincheck ?(
            
            <>
                
                <div className='LOGOcontainer'>
                <Image
                    priority
                    src='/images/LOGO.png' 
                    height={50}
                    width={50}
                    alt="0"
                    className='LOGOcontainer_1'
                />
                <span className='LOGOcontainer_2'>手勢辨識網站</span>
                <button className='LOGOcontainer_3'>{ buttommsg }</button>
                <Image
                    priority
                    src = { headimgurl }
                    height={50}
                    width={50}
                    alt="headimg"
                    className='LOGOcontainer_1'
                />
                </div>
                <h1>登入</h1>
            </>

            ):(

            <>
                <Image
                    priority
                    src='/images/LOGO.png' 
                    height={50}
                    width={50}
                    alt="0"
                />
                <span>手勢辨識網站</span>
                <button>{ buttommsg }</button>
                <h1>未登入</h1>
                
            </>
            
            )}

        </div>

    );
}