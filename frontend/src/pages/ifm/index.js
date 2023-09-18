import Head from "next/head";
import Image from "next/image";
import LoginState from "../../components/loginstate"
import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Link from "next/link";

export default function Ifm () {
    const router = useRouter();
    const [headiImageURL, setHeadiImageURL] = useState("");
    const [describe, setDescribe] = useState("");
    const [username, setUsername] = useState("");
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
            <Head>
                <title>個人資料</title>
            </Head>
            <LoginState
                profilePath="./ifm"
                resetPasswordPath="../reg/resetpassword"
                logoutPath="../"
            />
            <div className="profilecard" style={{border:'3px solid red'}}>
                <Image
                    src={ headiImageURL }
                    alt="頭圖"
                    height={45}
                    width={45}
                    priority
                /><span style={{fontSize:'30px'}}>{ username }</span>
                <p>{ describe }</p>
                
            </div>
            <h1>個人資料</h1>
            <div></div>
            <button>
                修改個人資料
            </button>
            <Link href={'./ifm/card'}>
                個人字卡
            </Link>
            <button>
                學習狀況評估
            </button>
        </>
    );

}