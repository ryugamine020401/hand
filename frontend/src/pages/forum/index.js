import { useEffect, useState } from "react";
import Head from "next/head";
import Link from "next/link";
import LoginState from "@/components/loginstate";



export default function Billboard(){
    const [title, setTitle] = useState({});

    const initialSetPage = async () =>{
        try {
            const response = await fetch("http://127.0.0.1:8000/forum/api/",{
                method:'GET',
            });

            if (response.status === 200){
                const responseData = await response.json();
                console.log(responseData);
                setTitle(responseData.title);
            } else {
                const responseData = await response.json();
                console.log(responseData);
            }
        } catch (error) {
            console.error(error)
        }

    }

    useEffect(() => {
        initialSetPage();        
    }, []);
    
    return(
        <>  
            <Head><title>公告欄</title></Head>
            
            <LoginState
                profilePath="./ifm"
                resetPasswordPath="../reg/resetpassword"
                logoutPath="./"

            />
            <h1>公告欄</h1>
            {Object.keys(title).map((key, index)=>(
                <div key={`billboardcontainer_${index}`}>
                
                    <Link key={`bill_link_${index}`} href={`./forum/${key}`}>{title[key]}</Link>
                
                </div>
            ))}

        </>
    );
}