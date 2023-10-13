import Image from 'next/image';
import { useState, useEffect } from 'react';
import Style from './loginstate.module.css';
import { useRouter } from 'next/router';
import OverlayBox from './overlay'
/* 
<LoginState
    profilePath="../../ifm"
    resetPasswordPath="./"
    logoutPath=""
/> 
*/
export default function LoginState({children, profilePath, resetPasswordPath, logoutPath}) {
    const nginxDomain = process.env.NEXT_PUBLIC_NGINX_DOMAIN
    const [logincheck, setLogincheck] = useState(false);
    const [headimgurl, setHeadImgURL] = useState(`${nginxDomain}/ifm/getmedia/headimage/guester.png`)
    const [buttommsg, setButtommsg] = useState("")
    const [showOverlay, setShowOverlay] = useState(false)
    const router = useRouter()
    
    function logindDirect (){
        router.push('http://127.0.0.1:3000/reg/login');
    }
    const jumpMenu = () => {
        console.log(showOverlay)
        setShowOverlay(!showOverlay)
    }
    const sendPostRequest = async () => {  

        try{
            const access_token = localStorage.getItem('access_token');
            const response = await fetch(`${nginxDomain}/reg/api/logincheck`,{

                method: "POST",
                headers:{
                    "Content-Type": "application/json",
                    "Authorization": `Beaer ${access_token}`,
                },
            });
            if (response.status === 200){
                // 驗證成功，具有登入狀態。
                const responseData = await response.json();
                //console.log(responseData.loginstatus);
                //console.log(responseData.headimgurl);
                setLogincheck(responseData.loginstatus);
                setButtommsg(responseData.buttom_word);
                setHeadImgURL(responseData.headimgurl);
            } else {
                // 驗證失敗，無登入狀態或過期。
                const responseData = await response.json();
                if (response.status === 403){
                    console.log(responseData.detail);
                    setButtommsg("登入");
                    const currentURL = window.location.href;
                    console.log('網址是:', currentURL);
                    localStorage.clear('access_token');
                    localStorage.clear('refresh_token');
                    
                    // router.push('http://127.0.0.1:3000/uchi');
                } else if (response.status === 401) {
                    console.log(responseData.message, '帳號沒有驗證');
                    router.push('http://127.0.0.1:3000/reg/valemail');
                    
                } else {
                    console.log(responseData.message)
                }
                setLogincheck(responseData.loginstatus);
                setButtommsg(responseData.buttom_word);
                setHeadImgURL(`${nginxDomain}/ifm/getmedia/headimage/guester.png`);
                
            }
        } catch(error) {
            
            console.log('有錯');
            console.log(error);
            
        }

    };

    const goHomeFunvrion = () =>{
        router.push('http://127.0.0.1:3000/uchi');
    }

    useEffect(()=>{
        
        sendPostRequest();
    }, [logincheck])
    
    return(

        <div className={Style.navbar}>
            {logincheck ?(
            
            <>
                
                <header className={Style.HeaderContainer}>
                <div className = {Style.LOGOcontainer} onClick={goHomeFunvrion}>
                    <Image
                        priority
                        src='/images/LOGO.png' 
                        height={50}
                        width={50}
                        alt="0"
                        className={Style.HeaderContainer_1}
                    />
                    <span className={Style.HeaderContainer_2}>手勢辨識網站</span>
                </div>
                <div className= {Style.LOGOcontainer2}>
                    <div className={Style.HeaderContainer_3}>
                        <Image
                            priority
                            src = { headimgurl }
                            height={45}
                            width={45}
                            alt="headimg"
                            className= {Style.HeadImage}
                            onClick={jumpMenu}
                        />
                    </div>
                    <p className={Style.HeaderContainer_4}>{ buttommsg }</p>
                </div>
                
                </header>
                {/* <h1>登入</h1> */}
                {showOverlay && 
                <OverlayBox
                    profilePath={profilePath}
                    resetPasswordPath={resetPasswordPath}
                    logoutPath={logoutPath}
                />}
            </>

            ):(

            <>
                <header className={Style.HeaderContainer}>
                <div className = {Style.LOGOcontainer} onClick={goHomeFunvrion}>
                    <Image
                        priority
                        src='/images/LOGO.png' 
                        height={50}
                        width={50}
                        alt="0"
                        className={Style.HeaderContainer_1}
                    />
                    <span className={Style.HeaderContainer_2}>手勢辨識網站</span>
                </div>
                <div className= {Style.LOGOcontainer2}>
                    <div className={Style.HeaderContainer_3}>
                        <Image
                            priority
                            src = { headimgurl }
                            height={45}
                            width={45}
                            alt="headimg"
                            className= {Style.HeadImage}
                        />
                    </div>
                    <p className={Style.HeaderContainer_4} id={Style.loginbuttom} onClick={logindDirect}>登入</p>
                </div>
                
                </header>
                
                {/* <h1>未登入</h1> */}
                
            </>
            
            )}
            <main>{children}</main>
        </div>

    );
}