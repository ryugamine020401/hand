import Style from './loginstate.module.css'
import Link from 'next/link';
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
    const logOut = () =>{
        localStorage.clear('access_token')
        localStorage.clear('refresh_token')
        router.reload()
    }
    return (
      <div className={Style.overlayContainer} >
        <div className={Style.overlayBox}>
            <ul className= {Style.UL}>
                <li><Link href= {profilePath}>個人資料</Link></li>
                <li><Link href= {resetPasswordPath}>重設密碼</Link></li>
                <li><Link href= {logoutPath} onClick={logOut}>登出</Link></li>
                <li>4</li>
            </ul>
        </div>
        </div>
    );
  };