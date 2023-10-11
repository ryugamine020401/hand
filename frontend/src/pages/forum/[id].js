// pages/[id].js

import LoginState from '@/components/loginstate';
import { Tillana } from 'next/font/google';
import Head from 'next/head';
import Image from 'next/image';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import style from '@/pages/forum/css/detial.module.css'
function DynamicPage() {
  	const router = useRouter();
  	const { id } = router.query;
	const [title, setTitle] = useState();
	const [content, setContent] = useState();
	const [authorname, setAuthorname] = useState();
	const [responsehint, setResponsehint] = useState('');
	const [userResponse, setuUserResponse] = useState();
	const [date, setDate] = useState();
	const [articalheadimage, setArticalHeadimage] = useState();
	const [response, setResponse] = useState();
	const [logincheck, setLogincheck] = useState();
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
				setAuthorname(responseData.authorname);
				console.log(responseData.response);
			} else {
				const responseData = await response.json();
				console.log(responseData);
			}
		} catch (error) {
			console.error(error);
		}
	}
	const sendUserResponsebuttonClick = async () => {
		try {
			const access_token = localStorage.getItem('access_token');
			const response = await fetch(`http://127.0.0.1:8000/forum/api/${id}/`,{
				method:'POST',
				body:JSON.stringify({userResponse}),
				headers:{
					'Authorization': `$Bearer ${access_token}`,
					'Content-Type':'Application/json',
				}
			});
			if (response.status === 200) {
				const responseData = await response.json();
				console.log(responseData);
				router.reload();
			} else {
				const responseData = await response.json();
				console.log(responseData);
			}

		} catch (error) {
			console.error(error)
		}
	}
	const checklogin = () => {
		const access_token = localStorage.getItem('access_token');
		if (access_token === null){
			setResponsehint('登入後方可留言。');
			setLogincheck(false);
 		} else {
			setResponsehint('');
			setLogincheck(true);
		}
	}
    useEffect(()=>{
		checklogin();
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
			<div className={style.detailpagecontainer}>
			
				<div className={style.contnetcontainer}>
					<div className={style.uppercontainer}>
						<div className={style.rightcontainer}>
							<h1>{title}</h1>
						</div>
						<div className={style.leftcontainer}>
						<Image
							alt = "發文者頭像"
							src = {articalheadimage}
							width={80}
							height={80}
						/>
						<p>{authorname}</p>
						<h6>{date}</h6>
						</div>
						
					</div>
					<hr></hr>
					<div className={style.lowercontainer}>
						<textarea 
							disabled={true}
							value={content}
						/>
					</div>
				</div>
				<div className={style.responseArea}>
					{response && 
						<div className='response'>
							{Object.keys(response).map((id, index) => (
								<div key={`test${index}`} className={style.responsecontainer}>
									<div className={style.responseuppercontainer}>
										<Image
											alt = "回覆者的頭像"
											width = {50}
											height = {50}
											src = {response[id].headimagUrl}
										/>
										<p key={`response_name_${index}`}>{response[id].username}  </p>
										<span key={`response_date_${index}`}>{response[id].upload_date}</span>
									</div>
									<div className={style.responselowercontainer}>
										<p key={`response_content_${index}`}>{response[id].response}</p>
									</div>
									
									

								</div>
								
							))}

						</div>}

						<div className={style.usersendResponsecomtainer}>
								<textarea 
									id="content"
									name="content"
									required
									defaultValue={responsehint}
									onChange={(e)=>setuUserResponse(e.target.value)}
									disabled={!logincheck}
								/>
								<button
									onClick={sendUserResponsebuttonClick}
									disabled={!logincheck}
								>
									送出回復
								</button>
						</div>
				</div>
			</div>	
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
