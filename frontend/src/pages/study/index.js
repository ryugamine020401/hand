import LoginState from "@/components/loginstate";
import Head from "next/head";
import Link from "next/link";
import style from '@/pages/study/indes.module.css'
import { useEffect, useState } from "react";
import { useRouter } from "next/router";

export default function Studyindex() {
    const router = useRouter();
    // const [page, setPage] = useState(1);
    const {page} = router.query;
    const pageNumber = page ? parseInt(page, 10) : 1;
    const resource = {
        'english' : '英文字母',
        'testtype/1/q0' : '測試1',
        'testtype/2/q0' : '個人字卡',
        'testtype/3/q0' : '測試3',
        'testtype/4/q0' : '測試4',
        'testtype/5/q0' : '測試5',
        'testtype/6/q0' : '測試6',
        'testtype/7/q0' : '測試7',
        'testtype/8/q0' : '測試8',     
        'testtype/9/q0' : '測試9',
        'testtype/10/q0' : '測試10',
        'testtype/11/q0' : '測試11', 
        'testtype/12/q0' : '測試12',
        'testtype/13/q0' : '測試13',  
    };
    const linklist = [
        'study/english', 'study/testtype/1/q0', 'ifm/card',
        'study/english', 'study/testtype/1/q0', 'ifm/card',
        'study/english', 'study/testtype/1/q0', 'ifm/card',
        'study/english', 'study/testtype/1/q0', 'ifm/card',
        'study/english', 'study/testtype/1/q0', 'ifm/card',
        'study/english', 'study/testtype/1/q0', 'ifm/card',
        
    ]
    const buttonChickfunction = (index) =>{
        router.push(`${linklist[index]}`);
    }

    const initialChecking = async () => {
        const acccess_token = localStorage.getItem('access_token');

        try {
            const response = await fetch("",{
                method:'GET',
                headers:{
                    'Atiorization':`Bearer ${acccess_token}`,
                }
            });
            if (response.status === 200){
                const responseData = await response.json();
                console.log(responseData);
            } else {
                const responseData = await response.json();
                console.log(responseData);
            }

        } catch (error) {
            console.log(error);
        }
    }
    useEffect(() => {
        initialChecking();
        console.log(pageNumber);
    },[])

    return(
    
        <>
            <Head><title>學習資源</title></Head>
            <LoginState
                    profilePath="../ifm"
                    resetPasswordPath="./reg/resetpassword"
                    logoutPath="./uchi"
            />
            <div className={style.studypagecontainer}>
                
                <div className={style.blackboardcontainer}>
                    {Object.keys(resource).slice(6*(pageNumber-1), pageNumber*6).map((key, index)=>(
                    <div key={`study_linkcontainer_${index}`} className={style.techtypecontainer} onClick={()=>buttonChickfunction(index)}>
                        <Link key={`study_link_${index}`} href={`./study/${key}`}>{resource[key]}</Link>
                    </div>
                    ))}
                </div>
                <a href={`./study?page=${pageNumber-1 <= 0 ? 1: pageNumber-1}`}>上一頁</a>
                <a href={`./study?page=${linklist.length > pageNumber*6? pageNumber+1 : pageNumber}`}>下一頁</a>
            </div>
            
        </>
    );

}