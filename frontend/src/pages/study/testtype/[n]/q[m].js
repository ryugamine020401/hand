// pages/test/testtype/[n]/q[m].js

import LoginState from '@/components/loginstate';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { useRef, useEffect, useState } from 'react';
import Webcam from 'react-webcam';
import style from '@/pages/study/css/q.module.css'
// import RecordRTC from 'recordrtc';
import dynamic from 'next/dynamic'

const VideoRecordingDialog = dynamic(() => import('./VideoRecordingDialog'), { ssr: false });


function TestPage() {
	/* ------------------------------------------- 測驗二 --------------------------------------------- */
	
	const [recording, setRecording] = useState(false);
	const [recordedVideo, setRecordedVideo] = useState(null);
	let recordRTC = null;
	const startRecording = () => {
		setRecording(true);
		recordRTC = RecordRTC(webcamRef.current.stream, {
			type: 'video',
		});
		recordRTC.startRecording();
		
		setTimeout(() => {
			stopRecording();
		}, 5000);
	};


	const stopRecording = () => {
		setRecording(false);
		if (recordRTC) {
			recordRTC.stopRecording(() => {
				const blob = recordRTC.getBlob();
				const reader = new FileReader();
		
				reader.onload = () => {
				const base64Video = reader.result;
				setRecordedVideo(base64Video);
				};
		
				reader.readAsDataURL(blob);
			});
		}
	};
	useEffect(() => {
		if (recording) {
		  const recordingTimeout = setTimeout(() => {
			stopRecording();
		  }, 5000);
	
		  return () => {
			clearTimeout(recordingTimeout);
		  };
		}
	  }, [recording]);

	/* ------------------------------------------- 測驗二 --------------------------------------------- */

	/* ------------------------------------------- 測驗一 --------------------------------------------- */
	const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
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
			const response = await fetch(`${backedUrl}/study/api/test/${n}/${parseInt(m.replace("q", ""), 10)}/`,{
				method:'POST',
				body:JSON.stringify({imageBase64, ans}),
				headers:{
					'Authorization':`Bearer ${access_token}`,
					'Content-Type' :'application/json'
				}
			});
			if (response.status === 200) {
				const responseData = await response.json();
				// console.log(responseData);
				setImageBase64('');
				router.push(`/study/testtype/${n}/q${parseInt(m.replace("q", ""), 10)+1}`);
			} else {
				const responseData = await response.json();
				// console.log(responseData);
				setErrorMsg(responseData.message);	
			}
		} catch (error) {
			// console.log(error);
		}
	}

	const StartTestButtonClick = async() => {
		const access_token = localStorage.getItem('access_token');
		try {
			const response = await fetch(`${backedUrl}/study/api/test/${n}/${parseInt(m.replace("q", ""), 10)+1}/`,{
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
				router.push(`/study/testtype/${n}/q${parseInt(m.replace('q',"", 10))+1}`);
			} else {
				const responseData = await response.json();
				console.log(responseData);
				router.reload();
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
		const response = await fetch(`${backedUrl}/study/api/test/${n}/${parseInt(m.replace("q", ""), 10)}/`, {
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
			// console.log(ans);
		} else {
			const responseData = await response.json();
			// console.log(responseData);
			if (response.status === 302) {
				setCheckQuestion(false);
				console.log(responseData.message);
				router.push(responseData.push);
			} else {
				
			}
			
		}
	} 

	useEffect(()=>{
		// loginstatetest();
		// console.log('一')
		// // console.log(parseInt(m.replace("q", ""), 10));
		if (n && m) {
			getQueation();
			// console.log(`n: ${n}, m: ${m}`);
			// console.log(parseInt(m.replace("q", ""), 10));
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
		if (n == 1) {
			btnRef.current.focus();
		}
		
	
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
  /* ------------------------------------------- 測驗一 --------------------------------------------- */
  return (
    <div>
      	<Head><title>測驗</title></Head>
      	<LoginState
			profilePath="../../../ifm"
			resetPasswordPath="../../../reg/resetpassword"
			logoutPath="../../../uchi"
		/>
		 
		{!checkquestion&& n == 1 &&
			<div className={style.testillustratepagecontainer}>
				<button className={style.repagebtn} onClick={()=>router.push('../../')}>上一頁</button>
				{/* <h1>{ans}</h1> */}
				<div className={style.illustratecontainer}>
					<h1>測驗說明</h1>
					<p>畫面上會出現有的小寫字母，使用者需要開啟相機並比出相應的手勢，</p>
					<p>比出正確手勢後，點擊<b>完成作答</b>或<b>按下Enter鍵</b>後進入下一題。</p>
					<p>若作答一半退出頁面視為未完成作答，此次測驗作廢，下次測驗會重置。</p>
					<p>考試隨機出題，一共五題。</p>
					<p>開始測驗後，系統會提示是否開啟相機，請選擇開啟。</p>
					<p></p>
					<button onClick={()=>StartTestButtonClick()} ref={btnRef}>點擊開始考試</button>
				</div>
				
			</div>
		}
		{checkquestion&& n == 1 &&
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
		{n == 2 &&
			<div >
				{parseInt(m.replace("q", ""), 10) != 0 &&<h1 className={style.test2pageH1}>第 {questionNum} 題 : 請比出 {ans} 的手語!</h1>}
				<VideoRecordingDialog/>
				
			</div>
			
		}

		{n == 2 && parseInt(m.replace("q", ""), 10) == 0 &&
			<div className={style.testillustratepagecontainer}>
				<button className={style.repagebtn} onClick={()=>router.push('../../')}>上一頁</button>
				{/* <h1>{ans}</h1> */}
				<div className={style.illustratecontainer}>
					<h1>測驗說明</h1>
					<p>畫面上會出現有的英文單字，使用者需要開啟相機並比出相應的手語，</p>
					<p>比出正確手語後，點擊<b>完成作答</b>或<b>按下Enter鍵</b>後進入下一題。</p>
					<p>若作答一半退出頁面視為未完成作答，此次測驗作廢，下次測驗會重置。</p>
					<p>考試隨機出題，一共五題。</p>
					<p>開始測驗後，系統會提示是否開啟相機，請選擇開啟。</p>
					<p></p>
					<button onClick={()=>StartTestButtonClick()} ref={btnRef}>點擊開始考試</button>
				</div>
			</div>}

	</div>
  );
}

export default TestPage;