import LoginState from "@/components/loginstate";
import { useRouter } from "next/router";
import { useEffect, useState, useRef } from "react";
import Head from "next/head";
import Cropper from 'react-cropper';
import 'cropperjs/dist/cropper.css';
import Style from './components/crop.module.css'
import style from '@/pages/ifm/css/remeishi.module.css'


export default function ReMeishi(){
    const backedUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const router = useRouter();
    const [username, setUsername] = useState("");
    const [describe, setDescribe] = useState("");
    const [birthday, setBirthday] = useState("");
    const [imageName, setImageName ] = useState("crop.jpg");
    const [headiImageURL, setHeadiImageURL] = useState("");
    const cropperRef = useRef(null);
	const [headimage, setHeadimage] = useState("");
	const [croppedImageDatasrc, setcroppedImageDatasrc] = useState('');
	const [cropenable, setCropEnable] = useState(false);

    const fetchImageAndConvertToBase64 = async (imageUrl) => {
        try {
          const response = await fetch(imageUrl);
          if (response.status === 200) {
            const blob = await response.blob();
            const base64Data = await new Promise((resolve, reject) => {
              const reader = new FileReader();
              reader.onloadend = () => resolve(reader.result);
              reader.onerror = reject;
              reader.readAsDataURL(blob);
            });
            setHeadimage(base64Data);
            return base64Data;
          } else {
            console.error('加载图片失败:', response.status);
            return null;
          }
        } catch (error) {
          console.error('加载图片失败:', error);
          return null;
        }
      };
      
    const getUserInformation = async() => {
        const access_token = localStorage.getItem('access_token');
        try {
            const response = await fetch(`${backedUrl}/ifm/api/userinformation`,{
                method:"GET",
                headers:{
                    "Authorization" : `Bearer ${access_token}`,
                }
            })

            if (response.status === 200) {
                const responseData = await response.json();
                console.log("有");
                setHeadiImageURL(responseData.headimageurl);
                setUsername(responseData.username);
                setDescribe(responseData.describe);
                fetchImageAndConvertToBase64(responseData.headimageurl);
                console.log(responseData.message);
                console.log('預設',headimage);
            } else if(response.status === 403){
                
                localStorage.clear('access_token');
                localStorage.clear('refresh_token');
                router.push('../uchi');
            } else {
                const responseData = await response.json();
                console.log(responseData)
            }
        } catch (error) {
            console.log(error);
        }
    }

    const handleUpload = (e) => {
		e.preventDefault();
		const fileInput = document.getElementById('fileInput');
		fileInput.click();

	};

	const handleFileChange = (e) => {
		setcroppedImageDatasrc('');
        getUserInformation();
		setCropEnable(true);
		const file = e.target.files[0];
		const reader = new FileReader();

		reader.onload = (event) => {
            const dataURL = event.target.result;
            cropperRef.current.cropper.replace(dataURL);

            const img = new Image();
            img.src = dataURL;
            img.onload = () => {
                console.log('高度：', img.height);
                console.log('寬度：', img.width);
            }
		}

		try {
			reader.readAsDataURL(file);
		} catch (error) {
			console.error(error);
            setCropEnable(false);
            getUserInformation();
		}
		
	};

	const handleCrop = () => {
		const croppedImageData = cropperRef.current.cropper.getCroppedCanvas().toDataURL();
		
		setcroppedImageDatasrc(croppedImageData);
        setHeadiImageURL(croppedImageDatasrc);
		setHeadimage(croppedImageData);
		setCropEnable(false);
		
	};
	const uploadImage = async () =>{
		const access_token = localStorage.getItem('access_token');
		try {
			const response = await fetch(`${backedUrl}/ifm/api/reMeishi`, {
				method:'POST',
				body:JSON.stringify({headimage}),
				headers:{
					'Authorization':`Bearer ${access_token}`,
					'Content-Type':'application/json'
				}            
			});
			if(response.status === 200){
				const responseData = await response.json();
				console.log(responseData);

			} else {
				const responseData = await response.json();
				console.log(responseData);
			}
		} catch (error) {
			console.error(error);
		}
	}
    
    useEffect(()=>{
        const access_token = localStorage.getItem('access_token');
        if (access_token === null){
            router.push('../uchi');
        }
        console.log(access_token);
        getUserInformation();
    },[]);
    

    const uploadButtonClick = async () =>{

        if(username != "" && birthday != "" && describe != ""){
            console.log("都有東西");
        } else {
            alert('欄位不得為空')
            console.log("沒有足夠的東西");
            return;
        }

        // console.log(imageName);

        try {
            const access_token = localStorage.getItem('access_token');
            const response = await fetch(`${backedUrl}/ifm/api/reMeishi`,{
                method:"POST",
                body:JSON.stringify({username, birthday, describe, imageName, headimage}),
                headers:{
                    'Content-Type' : 'application/json',
                    'Authorization': `Bearer ${access_token}`,
                }

            });
            if(response.status === 200){
                const responseData = await response.json();
                console.log(responseData.message);
                router.push('./');
            } else {
                const responseData = await response.json();
                console.log(responseData.message);
            }
            
        } catch (error) {
            console.error(error);
        }

    }
    
    return(
        <>  {/* 在這裡 ./ 就會是{base}/app/ 所以這裡是 {base}/ifm*/}
            
            <LoginState
                profilePath="./"
                resetPasswordPath="../reg/resetpassword"
                logoutPath="../uchi"
            />
            <div className={style.remeishipagecontainer}>
                <Head><title>修改個人資料</title></Head>
                <button className={style.repagebtn} onClick={()=>router.push('./')}>上一頁</button>
                <div className={style.formcontianer}>
                    <div className={style.uppercontainer}>
                        <div className={style.headimgcontainer}>
                            {croppedImageDatasrc ?( 
                            <img
                                src={ croppedImageDatasrc }
                                alt="頭圖_裁剪後"
                                priority
                                className={style.headimage}
                            /> 
                            ):(
                                <img
                                    // src={ croppedImageDatasrc }
                                    src={ headiImageURL }
                                    alt="頭圖_裁減前"
                                    priority
                                    className={style.headimage}
                                />
                            )}
                            <input
                                type="file"
                                id="fileInput"
                                accept="image/*"
                                onChange={handleFileChange}
                                style={{ display: 'none' }}
                            />
                            {!cropenable && <button onClick={handleUpload}>上傳圖像</button>}
                            <div className={style.cropcontainer}>
                                {!croppedImageDatasrc && <Cropper
                                    ref={cropperRef}
                                    className={Style.test}
                                    // style={{height:100, width:'50%'}}
                                    aspectRatio={1}
                                    zoomable={false}
                                    id="itmememememe"
                                />}
                                {cropenable && <button onClick={handleCrop}>裁剪</button>}
                                {/* {croppedImageDatasrc && 
                                <>
                                    <div className={Style.imagecontainer}>
                                        <img 
                                            alt='裁圖'
                                            src={croppedImageDatasrc}
                                            className={Style.image}
                                        />
                                        
                                    </div> 
                                    <button onClick={uploadImage}>確定修改大頭貼</button>
                                </>} */}
                            </div>
                        </div>
                        <div className={style.describecontainer}>

                            <label>個人簡介</label>
                            <textarea
                                id="describe"
                                name="describe"
                                required
                                value={describe}
                                onChange={(e)=>setDescribe(e.target.value)}
                            />
                        </div>
                    </div>
                    
                    <div className={style.lowercontainer}>
                        <div className={style.usernamecontainer}>
                            <img src="/images/username.png" width={20} height={20} alt="emailicon"/>
                            <label>暱稱</label>
                            <input
                                type="text"
                                id="username"
                                name="username"
                                required
                                value={username}
                                onChange={(e)=>setUsername(e.target.value)}
                            />
                        </div>
                        
                        <div className={style.birthdaycontainer}>
                            <img src="/images/birthday.png" width={20} height={20} alt="emailicon"/>
                            <label>生日</label>
                            <input
                                type="date"
                                name="birthday"
                                value={birthday}
                                onChange={(e)=>setBirthday(e.target.value)}
                            />
                        </div>
                        <div>
                            <button
                                onClick={uploadButtonClick}
                                disabled={cropenable}
                            >
                                修改資料
                            </button>
                        </div>
                    </div>
                    
                    
                </div>
                <div className={style.dogimgcontainer}>
                    <img src="/images/ifm_remeshidog.png" alt="dogimg"/>
                </div>
                
            </div>
            
            
            

            
        </>
    );
}