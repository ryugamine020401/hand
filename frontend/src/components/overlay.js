import Style from './loginstate.module.css'
import Link from 'next/link';
import { useRouter } from 'next/router';
export default function OverlayBox () {
    const router = useRouter();
    const logOut = () =>{
        localStorage.clear('access_token')
        localStorage.clear('refresh_token')
        router.reload()
        router.push('./uchi')
    }
    return (
      <div className={Style.overlayContainer} >
        <div className={Style.overlayBox}>
            <ul className= {Style.UL}>
                <li><Link href= './uchi' onClick={logOut}>登出</Link></li>
                <li>2</li>
                <li>3</li>
                <li>4</li>
            </ul>
        </div>
        </div>
    );
  };