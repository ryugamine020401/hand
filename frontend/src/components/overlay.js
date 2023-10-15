import Style from './loginstate.module.css'
import Link from 'next/link';
import Image from 'next/image';
import { useRouter } from 'next/router';

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
    const logOut = () =>{
        localStorage.clear('access_token')
        localStorage.clear('refresh_token')
        router.reload()
    }
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
                <li>
                    <Image src="/images/logout.png" width={20} height={20} alt="resetpwdicon"/>
                    <span><Link href= {logoutPath} onClick={logOut}>登出</Link></span>
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