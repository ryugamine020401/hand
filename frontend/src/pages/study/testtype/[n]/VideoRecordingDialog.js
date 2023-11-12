// pages/test/testtype/[n]/q[m].js

import LoginState from '@/components/loginstate';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { useRef, useEffect, useState } from 'react';
import Webcam from 'react-webcam';
import style from '@/pages/study/css/VideoRecordingDialog.module.css'
import RecordRTC from 'recordrtc';

function RecordCamComponment() {
	const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  	const router = useRouter();
  	const { n, m } = router.query;
	const webcamRef = useRef(null);
	const btnRef = useRef(null);	// 用來進入考試頁面
    const checkm0 = parseInt(m.replace("q", ""), 10) === 0;
	// console.log(checkm0, n, m);
	const [recording, setRecording] = useState(false);
	const [recordedVideo, setRecordedVideo] = useState(null);

	let recordRTC = null;
	const startRecording = () => {
		setRemainingSeconds(5);
		setRecording(true);
        setRecordedVideo(null);
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
                    // console.log(base64Video);
				};
				reader.readAsDataURL(blob);
			});
            
		}
	};

	const [remainingSeconds, setRemainingSeconds] = useState(5);

    useEffect(() => {
        let timer;

        if (recording) {
        timer = setInterval(() => {
            setRemainingSeconds((prevSeconds) => prevSeconds - 1);

            if (remainingSeconds === 0) {
                stopRecording();
                clearInterval(timer);
            }
        }, 1000);
        }

        return () => {
        clearInterval(timer);
        };
    }, [recording, remainingSeconds]);

    const captureVideo = async() => {
        // console.log(recordedVideo);
		const access_token = localStorage.getItem('access_token');
		try {
			const response = await fetch(`${backedUrl}/study/api/test/${n}/${parseInt(m.replace("q", ""), 10)+1}/`,{
				method:'POST',
				body:JSON.stringify({recordedVideo}),
				headers:{
					'Authorization':`Bearer ${access_token}`,
					'Content-Type' :'application/json'
				}
			});
			if (response.status === 200){
				const responseData = await response.json();
				console.log(responseData);
				setRecordedVideo(null);
				router.push(`/study/testtype/${n}/q${parseInt(m.replace('q',"", 10))+1}`);
			} else {
				const responseData = await response.json();
				console.log(responseData);
			}
		} catch (error) {
			console.error(error);
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
				// console.log(responseData);
				setCheckQuestion(true);
				// router.push(`/study/testtype/${n}/q${parseInt(m.replace('q',"", 10))+1}`);
				router.push(`/study/testtype/${n}/q${parseInt(m.replace('q',"", 10))+1}`);
			} else {
				const responseData = await response.json();
				// console.log(responseData);
			}
		} catch (error) {
			console.error(error);
		}
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
			// console.log(responseData);
			// setAns(responseData.mondai);
			// console.log(ans);
		} else {
			const responseData = await response.json();
			// console.log(responseData);
			if (response.status === 302) {
				// setCheckQuestion(false);
				// console.log(responseData.message);
				router.push(responseData.push);
			} else {
				
			}
			
		}
	}
	useEffect(()=>{
		getQueation();

	},[])
  return (
    <div>
      	<Head><title>測驗</title></Head>
      	<LoginState
			profilePath="../../../ifm"
			resetPasswordPath="../../../reg/resetpassword"
			logoutPath="../../../uchi"
		/>

		
        {n == 2 && checkm0 &&
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
		
		{n == 2  && !checkm0 &&
			<div className={style.queationpagecontainer}>
				
				{/* <h1>第 {questionNum} 題 : 請比出 {ans} 的手語!</h1> */}
				<div className={style.upperconatiner}>
					<div className={style.leftcontainer}>
						<Webcam audio={false} ref={webcamRef} mirrored={false} className={style.camera}/>			
					</div>
					<div className={style.rightcontainer}>
                        {recordedVideo && (
                            <video controls className={style.camera}>
                                <source src={recordedVideo} type="video/webm" />
                            </video>
                        )}
					</div>
				</div>

                <div className={style.lowercontainer}>
                    {recording ? (
                        <>
                            {/* <button onClick={stopRecording}>停止錄製</button> */}
                        </>
                    ) : (
                        <button onClick={startRecording}>開始錄製</button>
                    )}
					{recordedVideo && <button onClick={()=>captureVideo()} className={style.button} ref={btnRef}>完成作答</button>}
                </div>
                
				{recording && 
				<div className={style.countdownumber}>
					{remainingSeconds}    
				</div>}
				
				
			</div>
		}
	</div>
  );
}

export default RecordCamComponment;