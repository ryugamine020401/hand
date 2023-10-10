// pages/[id].js

import LoginState from '@/components/loginstate';
import { Tillana } from 'next/font/google';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import style from '@/pages/billboard/detial.module.css'

function DynamicPage() {
  	const router = useRouter();
  	const { id } = router.query;
	const [title, setTitle] = useState();
	const [content, setContent] = useState();
	const [date, setDate] = useState();
	// console.log(1);

	const GetBillboardcontent = async () => {
		try {
			const response = await fetch(`http://127.0.0.1:8000/billboard/api/${id}/`, {
				method:'GET',
            });
			if (response.status === 200){
				const responseData = await response.json();
				console.log(responseData);
				setTitle(responseData.title);
				setDate(responseData.date);
				setContent(responseData.content);
			} else {
				const responseData = await response.json();
				console.log(responseData);
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
				logoutPath="./uchi"
			/>
			
			{/* <h1>這是動態頁面 {id}</h1> */}
			<div className={style.detailpagecontainer}>
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
