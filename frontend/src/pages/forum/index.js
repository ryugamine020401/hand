import { useEffect, useState } from "react";
import Head from "next/head";
import Link from "next/link";
import LoginState from "@/components/loginstate";
import style from '@/pages/forum/css/index.module.css'
import { useRouter } from "next/router";

export default function Billboard(){
    const nginxdomain = process.env.NEXT_PUBLIC_NGINX_DOMAIN;
    const [title, setTitle] = useState({});
    const router = useRouter();
    const {page} = router.query;
    const pageNumber = page ? parseInt(page, 10) : 1;

    const initialSetPage = async () =>{
        try {
            const response = await fetch(`${nginxdomain}/forum/api/`,{
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

    const buttonClick = (key) => {
        router.push(`forum/${key}`);
    }
    const ClickPostConent = () => {
        if (localStorage.getItem('access_token') === null) {
            router.push('reg/login');
        } else {
            router.push('forum/send');
        }
        
    }
    useEffect(() => {
        initialSetPage();        
    }, []);
    
    return(
        <>  
            <Head><title>討論區</title></Head>
            
            <LoginState
                profilePath="./ifm"
                resetPasswordPath="../reg/resetpassword"
                logoutPath="./"

            />
            <div className={style.forumindexpagecontainer}>
            <button className={style.repagebtn} onClick={()=>router.push('../uchi')}>回首頁</button>
                <div className={style.formcontainer}>
                    {Object.keys(title).slice(5*(pageNumber-1), pageNumber*5).map((key, index)=>(
                        <div key={`forumcontainer_${index}`} className={style.forumurlcontainer}
                            onClick={()=>buttonClick(key)}
                        >
                        
                            <Link key={`forum_link_${index}`} href={`./forum/${key}`}>{title[key]}</Link>
                        
                        </div>
                    ))}
                    <div className={style.forumurlcontainer} onClick={()=>ClickPostConent()}>
                        
                        <Link  href={`./forum/send`}>發佈文章</Link>
                    
                    </div>
                </div>
                <div className={style.chanhepagecontainer}>
                    <a href={`./forum?page=${pageNumber-1 <= 0 ? 1: pageNumber-1}`}>上一頁</a>
                    <span>{pageNumber}</span>
                    <a href={`./forum?page=${Object.keys(title).length > pageNumber*5? pageNumber+1 : pageNumber}`}>下一頁</a>
                    {/* <a href={`./forum?page=${pageNumber+1}`}>下一頁</a> */}
                </div>
                
            </div>

            

        </>
    );
}