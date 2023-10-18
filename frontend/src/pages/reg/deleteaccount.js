import LoginState from '@/components/loginstate';
import style from '@/pages/reg/css/deleteaccount.module.css'
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

export default function DeleaccountPage() {
    const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const [userinstance, setUserinstance] = useState({});
    const router = useRouter();

    const CheckAccessToken = async() => {
        try {
            const access_token = await localStorage.getItem('access_token');
            const response = await fetch(`${backedUrl}/billboard/api/rootcheck`,{
                method:'POST',
                headers:{
                    'Authorization':`Bearer ${access_token}`,
                }

            });
            if (response.status === 200) {
                const responseData = await response.json();
                console.log(responseData);
            } else {
                const responseData = await response.json();
                console.log(responseData);
                router.push('../uchi')
            }
        } catch (error) {
            console.log(error);
        }
    }

    const deleteAccountButtonClick = async (userId) => {
        console.log(userId);
        const access_token = localStorage.getItem('access_token');
        const response = await fetch(`${backedUrl}/reg/api/deleteaccount`,{
            method:"POST",
            body:JSON.stringify({userId}),
            headers:{
                'Authorization':`Bearer ${access_token}`,
                'Content-Type':'application/json',
            }
        });
        try {
            if (response.status === 200) {
                const responseData = await response.json();
                console.log(responseData.message);
                router.reload();
            } else {
                const responseData = await response.json();
                console.log(responseData.message);
            }
        } catch (error) {
            console.error(error);
        }
    }

    const getAllUserlist = async () => {
        const accessToken = localStorage.getItem('access_token');
        const response = await fetch(`${backedUrl}/reg/api/deleteaccount`,{
            method:'GET',
            headers:{
                'Authorization':`Bearer ${accessToken}`,
            }
        });
        try {
            if (response.status === 200) {
                const responseData = await response.json();
                console.log(responseData.message);
                console.log(responseData.alluserlist);
                setUserinstance(responseData.alluserlist);
            } else {
                const responseData = await response.json();
                console.log(responseData.message);
            }
        } catch (error) {
            console.error(error);
        }
    }

    useEffect(()=>{
        CheckAccessToken();
        getAllUserlist();
    },[]);
    return(
    <>
        <div className={style.pagecontainer}>
            <LoginState
                profilePath="../../ifm"
                resetPasswordPath="/reg/resetpassword"
                logoutPath=""
            />
            <div className={style.userlistcontianer}>
                {Object.keys(userinstance).map((key, index)=>(
                    <div key={`userinstance_${index}`} className={style.cardcontianer}>
                        <p>使用者名稱 :{key}</p>
                        <p>使用者 id :{userinstance[key]}</p>
                        <button onClick={()=>deleteAccountButtonClick(userinstance[key])}>刪除使用者</button>
                    </div>
                ))}
            </div>
        </div>

    </>
    );
}