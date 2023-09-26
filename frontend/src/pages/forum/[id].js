// pages/[id].js

import LoginState from '@/components/loginstate';
import { Tillana } from 'next/font/google';
import Head from 'next/head';
import Image from 'next/image';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

function DynamicPage() {
  	const router = useRouter();
  	const { id } = router.query;
	const [title, setTitle] = useState();
	const [content, setContent] = useState();
	const [date, setDate] = useState();
	const [articalheadimage, setArticalHeadimage] = useState();
	const [response, setResponse] = useState();
	// console.log(1);

	const GetArticalcontent = async () => {
		try {
			const response = await fetch(`http://127.0.0.1:8000/forum/api/${id}/`, {
				method:'GET',
            });
			if (response.status === 200){
				const responseData = await response.json();
				console.log(responseData);
				setTitle(responseData.articalTitle);
				setDate(responseData.uploadDate);
				setContent(responseData.articalContent);
				setArticalHeadimage(responseData.authorImageUrl);
				setResponse(responseData.response);
				console.log(responseData.response);
			} else {
				const responseData = await response.json();
				console.log(responseData);
			}
		} catch (error) {
			console.error(error);
		}
	}


    useEffect(()=>{
		GetArticalcontent();
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
			<div className='content'>
				<Image
					alt = "發文者頭像"
					src = {articalheadimage}
					width={80}
					height={80}
				/>
				<h2>{title}</h2>
				<h6>{date}</h6>
				<p style={{padding:100}}>{content}</p>
			</div>
			{response && 
				<div className='response'>
					{Object.keys(response).map((id, index) => (
						<div key={`test${index}`}>
							<Image
								alt = "回覆者的頭像"
								width = {30}
								height = {30}
								src = {response[id].headimagUrl}
							/>
							<span key={`response_date_${index}`}>{response[id].username}  </span>
							<span key={`response_date_${index}`}>{response[id].upload_date}</span>
							<div key={`response_content_${index}`}>{response[id].response}</div>

							{/* {index} */}
						</div>
						// <div key={`response_${id}`}>

						// Object.keys(response[id]).map((key, index)=>(
						// 	<div key={`response_content__${key}`}>
						// 		{/* <div key={`responsecontent_${response[index][key]}`}>{key}</div> */}
						// 		{response[id][key]}
						// 	</div>

						// ))

						// // </div>
					))}

				</div>}
    	</div>
	)
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
