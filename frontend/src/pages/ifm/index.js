import Head from "next/head";
import Image from "next/image";
import LoginState from "../../components/loginstate"
import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import style from "./css/index.module.css"



export default function Ifm () {
    const router = useRouter();
    const imgurl = ['/images/ifm_resetinformation.png', '/images/ifm_userwordcard2.png', '/images/ifm_viewresault.png']
    const imgclassname = [
        style.img_1,
        style.img_2,
        style.img_3,
    ]
    
    const [headiImageURL, setHeadiImageURL] = useState("");
    const [describe, setDescribe] = useState("");
    const [username, setUsername] = useState("");
    const resourceObject = {
        './ifm/remeishi': '修改個人資料',
        './ifm/card' : '個人字卡',
        './' : '學習狀況評估',
    }

    const divbtnclick = (index) =>{
        const redirectlist = [
            './ifm/remeishi',
            './ifm/card',
            './'
        ]
        console.log(redirectlist[index]);
        router.push(redirectlist[index]);
    }

    const getUserInformation = async() => {
        const access_token = localStorage.getItem('access_token');
        try {
            const response = await fetch("http://127.0.0.1:8000/ifm/api/userinformation",{
                method:"GET",
                headers:{
                    "Authorization" : `Bearer ${access_token}`,
                }
            })

            if (response.status === 200) {
                const responseData = await response.json();
                console.log("有");
                setHeadiImageURL(responseData.headimageurl);
                setUsername(responseData.username);
                setDescribe(responseData.describe);
                console.log(responseData.message);
            } else if(response.status === 403){
                
                localStorage.clear('access_token');
                localStorage.clear('refresh_token');
                router.push('./uchi');
            } else {
                const responseData = await response.json();
                console.log(responseData)
            }
        } catch (error) {
            console.log(error);
        }
    }

    useEffect(() => {
        
        const access_token = localStorage.getItem('access_token');
        if(access_token === null){
            router.push('./uchi');
        }
        getUserInformation();
    }, [])

    
    return(
        <>
            <LoginState
                profilePath="./ifm"
                resetPasswordPath="../reg/resetpassword"
                logoutPath="../"
            />
            <div className={style.ifmindexpagecontainer}>
                <Head>
                    <title>個人資料</title>
                </Head>
                <div className={style.profilecard}>
                    <div className={style.imagecontainer}>
                        <Image
                            src={ headiImageURL }
                            alt="頭圖"
                            height={45}
                            width={45}
                            priority
                        />
                    </div>
                    <div className={style.textcontainer}>
                        <div className={style.username}><span style={{fontSize:'30px'}}>{ username }</span></div>
                        <div className={style.describe}><p>{ describe }</p></div>
                    </div>
                    
                    
                </div>
                
                <div className={style.ifmtypecontainer}>
                {Object.keys(resourceObject).map((key, index)=>(
                    <div key={`ifmlinkdiv_${index}`} className={style.linkcontainer} onClick={()=>divbtnclick(index)}>
                        <Image
                            height={100}
                            width={100}
                            className={`${imgclassname[index]}`}
                            alt="圖片"
                            src={imgurl[index]}
                        />
                        <Link key={`ifmlink_${index}`} href={key} className={`${imgclassname[index]}`}>{resourceObject[key]}</Link>
                    </div>
                ))}
                </div>
            </div>       
        </>
    );

}