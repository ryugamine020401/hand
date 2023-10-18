import Style from './loginstate.module.css'
import Link from 'next/link';
import Image from 'next/image';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';


/* 
<LoginState
    profilePath="../../ifm"
    resetPasswordPath="./"
    logoutPath=""
/> 
*/
export default function OverlayBox ({ profilePath, resetPasswordPath, logoutPath }) {
    const router = useRouter();
    const nowUrlpath = router.pathname;
    const frontendURL = process.env.NEXT_PUBLIC_FRONTED_URL;
    const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const logOut = () =>{
        localStorage.clear('access_token');
        localStorage.clear('refresh_token');
        router.reload();
    }
    const [sendbillboardURL, setSendbillboardURL] = useState();
    const [sendteachimageURL, setSendteachimageURL] = useState();
    const [deleteaccount, setDeleteaccountURL] = useState();
    const CheckAccessToken = async() => {
        try {
            const access_token = await localStorage.getItem('access_token');
            const response = await fetch(`${backedUrl}/billboard/api/rootcheck`,{
                method:'POST',
                headers:{
                    'Authorization':`Bearer ${access_token}`,
                }
            });
            if (response.status === 200) {
                const responseData = await response.json();
                console.log(responseData);
                setSendbillboardURL(`${frontendURL}/billboard/send`);
                setSendteachimageURL(`${frontendURL}/study/uploadteachimage`);
                setDeleteaccountURL(`${frontendURL}/reg/deleteaccount`);
            } else {
                const responseData = await response.json();
                console.log(responseData);

            }
        } catch (error) {
            console.log(error);
        }
    }
    useEffect(()=>{
        CheckAccessToken();
    },[]);

    return (
      <div className={Style.overlayContainer} >
        <div className={Style.overlayBox}>
            <ul className= {Style.UL}>
                {nowUrlpath != '/ifm' &&
                <li>
                    <Image src="/images/password.png" width={20} height={20} alt="pwdicon"/>
                    <Link href= {profilePath}>個人資料</Link>
                </li>}
                {nowUrlpath != '/reg/resetpassword' &&
                <li>
                    <Image src="/images/resetpassword.png" width={20} height={20} alt="resetpwdicon"/>
                    <Link href= {resetPasswordPath}>重設密碼</Link>
                </li>}
                {sendbillboardURL && <li>
                    <Image src="/images/overlay_uploadimage.png" width={20} height={20} alt="resetpwdicon"/>
                    <Link href= {sendbillboardURL}>上傳公告</Link>
                </li>}
                {sendteachimageURL && <li>
                    <Image src="/images/overlay_billboard.png" width={20} height={20} alt="resetpwdicon"/>
                    <Link href= {sendteachimageURL}>上傳資源</Link>
                </li>}
                {deleteaccount &&   <li>
                    <Image src="/images/overlay_deleteaccount.png" width={20} height={20} alt="resetpwdicon"/>
                    <Link href= {deleteaccount}>刪除使用者</Link>
                </li>

                }
                <li>
                    <Image src="/images/logout.png" width={20} height={20} alt="resetpwdicon"/>
                    <Link href= {logoutPath} onClick={logOut}>登出</Link>
                </li>
            </ul>
        </div>
        {/* <div className={Style.overlayBox}>
            
            <button className={Style.btn1}>個人資料</button>
            <button className={Style.btn2}>重設密碼</button>
            <button className={Style.btn3}>登出</button>
            
        </div> */}
        
    </div>
    );
  };