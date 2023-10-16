import { useEffect, useState } from "react";
import Head from "next/head";
import Link from "next/link";
import LoginState from "@/components/loginstate";
import style from '@/pages/forum/css/index.module.css'
import { useRouter } from "next/router";

export default function Billboard(){
    const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const [title, setTitle] = useState({});
    const [nowPage, setNowPage] = useState(1);
    const router = useRouter();
    const {page} = router.query;
    const pageNumber = page ? parseInt(page, 10) : 1;

    const initialSetPage = async () =>{
        try {
            const response = await fetch(`${backedUrl}/forum/api/`,{
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

    const changePage = (cnt) => {
        //console.log(nowPage, cnt, nowPage+cnt);
        
        if (cnt >= 1) {
            /* 下一頁 */
            if (Object.keys(title).length > 5*(nowPage)){
                const nextPage = nowPage + cnt;
                setNowPage(nextPage);
                
            } else {

            }
        } else {
            /* 上一頁 */
            const nextPage = nowPage + cnt;
            if (nextPage <= 0) {
                setNowPage(1);
            } else {
                setNowPage(nextPage);
            }
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
                logoutPath="/uchi"

            />
            <div className={style.forumindexpagecontainer}>
            <button className={style.repagebtn} onClick={()=>router.push('../uchi')}>回首頁</button>
                <div className={style.formcontainer}>
                    {Object.keys(title).slice(5*(nowPage-1), nowPage*5).map((key, index)=>(
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
                    <button onClick={()=>changePage(-1)}>上一頁</button>
                    <a href={`./forum?page=${pageNumber-1 <= 0 ? 1: pageNumber-1}`}>上一頁</a>
                    <span>{nowPage}</span>
                    <a href={`./forum?page=${Object.keys(title).length > pageNumber*5? pageNumber+1 : pageNumber}`}>下一頁</a>
                    <button onClick={()=>changePage(1)}>下一頁</button>
                    {/* <a href={`./forum?page=${pageNumber+1}`}>下一頁</a> */}
                </div>
                
            </div>

            

        </>
    );
}