// pages/test/testtype/[n]/q[m].js

import LoginState from '@/components/loginstate';
import { parse } from 'cookie';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { useRef, useCallback, useEffect, useState } from 'react';
import Webcam from 'react-webcam';
import style from '@/pages/study/css/q.module.css'

function TestPage() {
  	const router = useRouter();
  	const { n, m } = router.query;
	const webcamRef = useRef(null);
	const [isCameraOn, setIsCameraOn] = useState(false);
	const [imageBase64, setImageBase64] = useState("");
	const [errormsg, setErrorMsg] = useState('');
	const [ans, setAns] = useState("");
	const [questionNum, setQuestionNum] = useState("");
	const [checkquestion, setCheckQuestion] = useState(false);
	const btnRef = useRef(null);	// 用來進入考試頁面
	const btn2Ref = useRef(null);	//

	const captureImage = () => {
		if (webcamRef.current) {
			const video = webcamRef.current.video;
			const canvas = document.createElement('canvas');
			const ctx = canvas.getContext('2d');
			canvas.width = 300;
			canvas.height = 300;
			ctx.drawImage(video, (video.videoWidth - 300) / 2, (video.videoHeight - 300) / 2, 300, 300, 0, 0, 300, 300);
			const imageDataURL = canvas.toDataURL('image/png');
			setImageBase64(imageDataURL);
			
			// postImagetoBackend();
		} else {
			console.error('Webcam video not available.');
		}
	}

	const postImagetoBackend = async() =>{
		try {
			const access_token = localStorage.getItem('access_token');
			const response = await fetch(`http://127.0.0.1:8000/study/api/test/${n}/${parseInt(m.replace("q", ""), 10)}/`,{
				method:'POST',
				body:JSON.stringify({imageBase64, ans}),
				headers:{
					'Authorization':`Bearer ${access_token}`,
					'Content-Type' :'application/json'
				}
			});
			if (response.status === 200) {
				const responseData = await response.json();
				console.log(responseData);
				setImageBase64('');
				router.push(`/study/testtype/${n}/q${parseInt(m.replace("q", ""), 10)+1}`);
			} else {
				const responseData = await response.json();
				console.log(responseData);
				setErrorMsg(responseData.message);	
			}
		} catch (error) {
			console.log(error);
		}
	}

	const StartTestButtonClick = async() => {
		router.push(`/study/testtype/${n}/q${parseInt(m.replace('q',"", 10))+1}`)
		const access_token = localStorage.getItem('access_token');
		try {
			const response = await fetch(`http://127.0.0.1:8000/study/api/test/${n}/${parseInt(m.replace("q", ""), 10)}/`,{
				method:'GET',
				headers:{
					'Authorization':`Bearer ${access_token}`,
					'Content-Type' :'application/json'
				}
			});
			if (response.status === 200){
				const responseData = await response.json();
				console.log(responseData);
				setCheckQuestion(true);
			} else {
				const responseData = await response.json();
				console.log(responseData);
			}
		} catch (error) {
			console.error(error);
		}
	}

	const loginstatetest = () => {
		const access_token = localStorage.getItem('access_token');
		if (access_token === null) {
			router.push('../../../uchi');
		}
		setIsCameraOn(true);
  	}

	const getQueation = async () => {
		// const access_token = localStorage.getItem('access_token');
		const access_token = localStorage.getItem('access_token');
		const response = await fetch(`http://127.0.0.1:8000/study/api/test/${n}/${parseInt(m.replace("q", ""), 10)}/`, {
			method:'GET',
			headers:{
				'Authorization':`Bearer ${access_token}`,
				'Content-Type' :'application/json'
			}
		});
		if (response.status === 200) {
			const responseData = await response.json();
			console.log(responseData);
			setAns(responseData.mondai);
			console.log(ans);
		} else {
			const responseData = await response.json();
			console.log(responseData);
			if (response.status === 302) {
				setCheckQuestion(false);
				console.log(responseData.message);
				router.push(responseData.push);
			} else {
				
			}
			
		}
	} 

	useEffect(()=>{
		loginstatetest();
		console.log('一')
		// console.log(parseInt(m.replace("q", ""), 10));
		if (n && m) {
			getQueation();
			console.log(`n: ${n}, m: ${m}`);
			console.log(parseInt(m.replace("q", ""), 10));
			setQuestionNum(parseInt(m.replace("q", ""), 10));
		}
		// isAllowedTransition();
	}, [n, m]);
  
	useEffect(()=>{
		if (imageBase64) {
			/* 送出影像 */
			postImagetoBackend();
		}
	},[imageBase64]);

	useEffect(() => {
		// 設定焦點在按鈕上
		btnRef.current.focus();
	
		// 監聽鍵盤事件，當按下 Enter 鍵時觸發點擊按鈕
		const handleKeyPress = (event) => {
		  if (event.key === 'Enter') {
			btnRef.current.click();
		  }
		};
	
		document.addEventListener('keydown', handleKeyPress);
		return () => {
			document.removeEventListener('keydown', handleKeyPress);
		  };
		
	  }, []);
  
  return (
    <div>
      	<Head><title>測驗</title></Head>
      	<LoginState
			profilePath="../../../ifm"
			resetPasswordPath="../../../reg/resetpassword"
			logoutPath="../../../uchi"
		/>
		{!checkquestion&&
			<div className={style.testillustratepagecontainer}>
				{/* <h1>{ans}</h1> */}
				<div className={style.illustratecontainer}>
					<h1>測驗說明</h1>
					<p>畫面上會出現有的字母，使用者需要開啟相機並比出相應的手勢，</p>
					<p>比出正確手勢後，點擊 完成作答 後進入下一題。</p>
					<p>若作答一半退出頁面會算未完成作答，無法繼續此次測驗，下次測驗會重製。</p>
					<p>考試隨機出題，一共五題。</p>
					<p>開始測驗後，系統會提示是否開啟相機，請選擇開啟。</p>
					<p></p>
					<button onClick={()=>StartTestButtonClick()} ref={btnRef}>點擊開始考試</button>
				</div>
				
			</div>
		}
		{checkquestion&&
			<div className={style.queationpagecontainer}>
				<h1>第 {questionNum} 題 : 請比出 {ans} 的手勢!</h1>
				<div>
					<div className={style.leftcontainer}>
						{checkquestion && 

						<div>
							<div className={style.videoContainer}>
								<Webcam audio={false} ref={webcamRef} mirrored={false} className={style.camera}/>			
							</div>
							
						</div>}
					</div>
					
					<div className={style.rightcontainer}>
						{imageBase64 && (
							<div>
							<img src={imageBase64} alt="Captured" />
							</div>
						)}
					</div>
				</div>
				
				<button onClick={()=>captureImage()} className={style.button} ref={btnRef}>完成作答</button>
				{imageBase64 && <p style={{"color":"red"}}>{errormsg}</p>}
			</div>
		}
		</div>
  );
}

export default TestPage;