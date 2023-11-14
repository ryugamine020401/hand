import Head from "next/head";
import Image from "next/image";
import style from "@/pages/study/css/result.module.css"
import LoginState from "@/components/loginstate";
import { useEffect, useState } from "react";
import { useRouter } from "next/router";

export default function Testresult(){
    const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const [correctNum , setCorrectNum] = useState(5);
    const [detial, setDetial] = useState([]);
    const router = useRouter();
    const getscore = async() =>{
        const access_token = localStorage.getItem('access_token');
        try {
            const response = await fetch(`${backedUrl}/study/api/testoneegetresult2`,{
                method:"GET",
                headers:{
                    'Authorization':`Bearer ${access_token}`
                }
            });
            if (response.status === 200) {
                const responseData = await response.json();
                // console.log(responseData);
                // console.log(responseData['point']);
                setCorrectNum(responseData.point);
                setDetial(responseData.detial);
            } else {
                const responseData = await response.json();
                // console.log(responseData);
            }
        } catch (error) {
            console.error(error);
        }
    } 
    
    useEffect(()=>{
        const access_token = localStorage.getItem('access_token');
        if (access_token === null) {
            router.push('../../reg/login');
        }
        getscore();
    }, []);

    return(
        <>
            <Head><title>測驗完成</title></Head>
                <div className={style.resultpagecontainer}>
                    <LoginState
                        profilePath="../../../ifm"
                        resetPasswordPath="../../../reg/resetpassword"
                        logoutPath="../../../uchi"
                    />
                    <div className={style.uppercontainer}>
                        <h1>您在這次試驗中答對了 {correctNum}/5 題。</h1>
                    </div>
                    <div className={style.lowercontainer}>
                        
                        <div className={style.leftcontainer2}>
                            <p className={style.fixtext}>您此次測驗的回答狀況</p>
                            {detial.map((index, cnt)=>(
                                (index[0] === index[1])?(
                                    <p key={`text_${index}`} >
                                    第{cnt+1}題 題目是 <span style={{"color":"blue"}}>{index[0]}</span> 您的回答是 <span style={{"color":"blue"}}>{index[1]}</span>
                                    </p>
                                ):(
                                    <p key={`text_${index}`}>
                                    第{cnt+1}題 題目是 <span style={{"color":"red"}}>{index[0]}</span> 您的回答是 <span style={{"color":"red"}}>{index[1]}</span>
                                    </p>
                                )
                            ))}
                        </div>
                        <div className={style.middlecontainer}>
                            <Image
                                src={`/images/study_test_start${correctNum}_girl.png`}
                                alt={"image"}
                                width={300}
                                height={400}
                            
                            />
                        </div>
                        <div className={style.rightcontainer}>
                            <button onClick={()=>router.push('../../ifm/allresultview')}>總測驗結果</button>
                            <button onClick={()=>router.push('./2/q0')}>重新測驗</button>
                            <button onClick={()=>router.push('../../uchi')}>返回首頁</button>
                        </div>
                    </div>
            </div>
        </>
    );
}