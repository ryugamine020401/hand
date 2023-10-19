// pages/[id].js

import LoginState from '@/components/loginstate';
import { Tillana } from 'next/font/google';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import style from '@/pages/billboard/css/detial.module.css'

function DynamicPage() {
	const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  	const router = useRouter();
  	const { id } = router.query;
	const [title, setTitle] = useState();
	const [content, setContent] = useState();
	const [date, setDate] = useState();
	const [button, setButton] = useState(false);
	// console.log(1);

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
                // const responseData = await response.json();
                // console.log(responseData);
				setButton(true);
            } else {
				// 不顯示按刪除文章按鈕
				setButton(false);
            }
        } catch (error) {
            console.log(error);
        }
    }
	useEffect(()=>{
        CheckAccessToken();
    },[])

	const GetBillboardcontent = async () => {
		try {
			const response = await fetch(`${backedUrl}/billboard/api/${id}/`, {
				method:'GET',
            });
			if (response.status === 200){
				const responseData = await response.json();
				console.log(responseData);
				setTitle(responseData.title);
				setDate(responseData.date);
				setContent(responseData.content);
			} else if(response.status === 302) {
				const responseData = await response.json();
				router.push(responseData.redirect);
			} else {
				const responseData = await response.json();
				console.log(responseData);
			}
		} catch (error) {
			console.error(error);
		}
	}
	const deleteContent = async(contentId)=>{
		console.log(contentId);
		const access_token = localStorage.getItem('access_token');
		const response = await fetch(`${backedUrl}/billboard/api/${contentId}/`, {
			method:'DELETE',
			body:JSON.stringify(contentId),
			headers:{
				'Authorization':`Bearer ${access_token}`,
				'Content-Type':'application/json'
			}
		});

		try {
			if (response.status === 200) {
				const responseData = await response.json();
				console.log(responseData.message);
				router.push('/billboard');
			} else {
				const responseData = await response.json();
				console.log(responseData.message);
			}
		} catch (error) {
			console.error(error);
		}
	}

    useEffect(()=>{
		GetBillboardcontent();
		// console.log(2);
    },[])
  // 根據不同的 id 值渲染不同的內容
  	return (

    	<div>
			<Head><title>{title}</title></Head>
			<LoginState
				profilePath="../ifm"
				resetPasswordPath="../reg/resetpassword"
				logoutPath="/uchi"
			/>
			
			{/* <h1>這是動態頁面 {id}</h1> */}
			<div className={style.detailpagecontainer}>
				<button className={style.repagebtn} onClick={()=>router.push('./')}>上一頁</button>
				<div className={style.mainareacontainer}>
					<div className={style.uppercontainer}>
						<h1>{title}</h1><h6>{date}</h6>
					</div>
					<div className={style.lowercontainer}>
						<textarea
						value={content}
						disabled
						/>
					</div>
					{button &&
						<button className={style.deletebutton} onClick={()=>deleteContent(id)}>刪除文章</button>
					}
					
				</div>
			</div>
			
			{/* <h6>{date}</h6>
			<p style={{padding:100}}>{content}</p> */}
    	</div>
  	);
}

export default DynamicPage;

export async function getServerSideProps(context) {
	const { params } = context;
	const id = params.id; // 從路由參數中獲取 id
	// console.log(4);
	// 在伺服器端發送 GET 請求以獲取數據，然後將 id 和數據傳遞給組件
	// 注意：這部分代碼只在伺服器端運行，而不在客戶端運行
	return {
	  props: {
		id,
	  },
	};
  }
