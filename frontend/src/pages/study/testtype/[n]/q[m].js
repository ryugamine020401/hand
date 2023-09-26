// pages/test/testtype/[n]/q[m].js

import LoginState from '@/components/loginstate';
import { parse } from 'cookie';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { useRef, useCallback, useEffect, useState } from 'react';
import Webcam from 'react-webcam';
import Style from './q.module.css'

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
			// console.log(imageBase64);
			postImagetoBackend();
			
		} else {

		}
		
	},[imageBase64]);
  
  return (
    <div>
      	<Head><title>測驗</title></Head>
      	<LoginState
			profilePath="../../../ifm"
			resetPasswordPath="../../../reg/resetpassword"
			logoutPath="../../../uchi"
		/>
		{!checkquestion&&
			<div>
				<h1>{ans}</h1>
				<button onClick={()=>StartTestButtonClick()}>點擊開始考試</button>
			</div>
		}
		
		{checkquestion && <div>
			<h1>第 {questionNum} 題 : 請比出 {ans} 的手勢!</h1>
			
			
			<div className={Style.videoContainer}>
				<Webcam audio={false} ref={webcamRef} mirrored={false} className={Style.camera}/>			
			</div>
			<button onClick={()=>captureImage()}>Capture Image</button>
		</div>}
		{imageBase64 && (
			<div>
			<h2>Captured Image</h2>
			<img src={imageBase64} alt="Captured" />
			<p>{errormsg}</p>
			</div>
		)}
		</div>
  );
}

export default TestPage;