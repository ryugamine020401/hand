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
    
    return (
      <div className={Style.overlayContainer} >
        <div className={Style.overlayBox}>
            <ul className= {Style.UL}>
                <li><Link href= {profilePath}>個人資料</Link></li>
                <li><Link href= {resetPasswordPath}>重設密碼</Link></li>
                <li><Link href= {logoutPath}>登出</Link></li>
                <li>4</li>
            </ul>
        </div>
        </div>
    );
  };