// pages/test/testtype/[n]/q[m].js

import LoginState from '@/components/loginstate';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { useRef, useEffect, useState } from 'react';
import Webcam from 'react-webcam';
import style from '@/pages/study/css/VideoRecordingDialog.module.css';
import lodingstyle from '@/pages/reg/css/register.module.css';
import RecordRTC from 'recordrtc';

function RecordCamComponment() {
	const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  	const router = useRouter();
  	const { n, m } = router.query;
	const webcamRef = useRef(null);
	const [errormsg, setErrorMsg] = useState('');
	const [loding, setLoding] = useState(false);
	const btnRef = useRef(null);	// 用來進入考試頁面
    const checkm0 = parseInt(m.replace("q", ""), 10) === 0;
	const [recording, setRecording] = useState(false);
	const [recordedVideo, setRecordedVideo] = useState(null);

	let recordRTC = null;
	const startRecording = () => {
		setErrorMsg('');
		setRemainingSeconds(3);
		setRecording(true);
        setRecordedVideo(null);
		recordRTC = RecordRTC(webcamRef.current.stream, {
			type: 'video',
		});
		recordRTC.startRecording();
		
		setTimeout(() => {
			stopRecording();
		}, 3000);
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

	const [remainingSeconds, setRemainingSeconds] = useState(3);

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
		setLoding(true);
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
				// console.log(responseData);
				setRecordedVideo(null);
				setLoding(false);
				router.push(`/study/testtype/${n}/q${parseInt(m.replace('q',"", 10))+1}`);
				
			} else if(response.status === 400){
				const responseData = await response.json();
				// console.log(responseData);
				setErrorMsg(responseData.message);
				setLoding(false);
			} else {
				const responseData = await response.json();
				// console.log(responseData);
			}
		} catch (error) {
			console.error(error);
		}
    }
  return (
    <div>
      	<Head><title>測驗</title></Head>
      	<LoginState
			profilePath="../../../ifm"
			resetPasswordPath="../../../reg/resetpassword"
			logoutPath="../../../uchi"
		/>
		
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
				{loding && <div className={lodingstyle.loader}/>}
				{<p style={{"color":"red" ,"margin-left":"36rem"}}>{errormsg}</p>}
				
			</div>
		}
	</div>
  );
}

export default RecordCamComponment;