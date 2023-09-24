import LoginState from "@/components/loginstate";
import Head from "next/head";
import Link from "next/link";
import { useEffect } from "react";

export default function Studyindex() {
    const resource = {
        'english' : '英文字母',
        'testtype/1/q1' : '測試1',
        'testtype/2/q2' : '測試2',        
    };
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
    },[])

    return(
    
        <>
            <Head><title>學習資源</title></Head>
            <LoginState
                profilePath="../ifm"
                resetPasswordPath="./reg/resetpassword"
                logoutPath="./uchi"
            />
            {Object.keys(resource).map((key, index)=>(
                <div key={`study_linkcontainer_${index}`}>
                    <Link className={`link_${index}`} key={`study_link_${index}`} href={`./study/${key}`}>{resource[key]}</Link>
                </div>
            ))}
        </>
    );

}