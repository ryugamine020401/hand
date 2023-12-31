
import style from '@/pages/ifm/css/allresultview.module.css'
import LoginState from '@/components/loginstate'
import Image from 'next/image'
import Head from 'next/head'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
export default function AllResultView(){
    const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const [headerImageUrl, setHeaderImageUrl] = useState('');
    const [result, setResult] = useState([]);
    const [result2, setResult2] = useState([]);
    const [starUrl1, setStar1] = useState(5);
    const [starUrl2, setStar2] = useState(5);     // 錯字 star
    const router = useRouter();
    const gobackbuttonClick = () =>{
        router.push('/ifm');
    }
    const initialsetup = async() =>{
        const access_token = localStorage.getItem('access_token');
        if (access_token === null) {
            router.push('../reg/login?nextpage=../ifm/allresultview');
        }
        try {
            const response = await fetch(`${backedUrl}/study/api/getallresult`,{
                method:"GET",
                headers:{
                    'Authorization':`Bearer ${access_token}`
                }
            });
            if (response.status === 200) {
                const responseData = await response.json();
                console.log(responseData.resultScore1);
                setHeaderImageUrl(responseData.headimageurl);
                setResult(responseData.resultScore1.toFixed(2));
                setResult2(responseData.resultScore2.toFixed(2));
                setStar1(responseData.star1);
                setStar2(responseData.star2);
            } else {
                const responseData = await response.json();
                // console.log(responseData);
            }
        } catch (error) {
            console.error(error);
        }
        
    }

    useEffect(()=>{
        initialsetup();
    },[]);
    return(
        <>
            <LoginState
                profilePath="./"
                resetPasswordPath="../../reg/resetpassword"
                logoutPath="../../"
            />
            <Head>
                    <title>學力報告書</title>
                </Head>
            <div className={style.allresultpagecontainer}>
                <div className={style.sheetcontainer}>
                    <div className={style.contianerone}>
                        <h1>學力報告書</h1>
                        <Image
                        alt = "頭像"
                        width={150}
                        height={150}
                        src={headerImageUrl}
                        />
                        <p>使用者暱稱</p>
                    </div>
                    <div className={style.contianertwo}>
                        <h3>測驗一的準確率</h3>
                        <div className={style.resultcontainer}>
                            <Image
                            alt="使用者評級圖像"
                            width={100}
                            height={130}
                            src={`/images/study_test_start${starUrl1}_boy.png`}
                            />
                            <p>您在測驗一的準確率為 {result} %</p>
                        </div>
                    </div>
                    <div className={style.contianerthree}>
                        <h3>測驗二的準確率</h3>
                        <div className={style.resultcontainer}>
                            <Image
                            alt="使用者評級圖像"
                            width={100}
                            height={130}
                            src={`/images/study_test_start${starUrl2}_boy.png`}
                            />
                            <p>您在測驗二的準確率為 {result2} %</p>
                        </div>
                    </div>
                    <div className={style.contianerfour}>
                        <h1>綜合評估您的學習能力</h1>
                        <Image
                            alt="使用者評級圖像"
                            width={300}
                            height={380}
                            src={`/images/study_test_start${((starUrl1+starUrl2)/2) === 0 ? (1):Math.floor((starUrl1+starUrl2)/2)}_boy.png`}
                        />
                        {console.log(starUrl2)}
                    </div>
                </div>
                <button className={style.gobackbutton} onClick={()=>gobackbuttonClick()}>上一頁</button>
            </div>
            
        </>
    )
}