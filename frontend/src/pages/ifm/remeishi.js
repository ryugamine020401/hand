import LoginState from "@/components/loginstate";
import { useRouter } from "next/router";
import { useEffect, useState, useRef } from "react";
import Head from "next/head";
import Cropper from 'react-cropper';
import 'cropperjs/dist/cropper.css';
import Style from './components/crop.module.css'


export default function ReMeishi(){
    const router = useRouter();
    const [username, setUsername] = useState("");
    const [describe, setDescribe] = useState("");
    const [birthday, setBirthday] = useState("");
    const [imageName, setImageName ] = useState("crop.jpg");
    const cropperRef = useRef(null);
	const [headimage, setHeadimage] = useState("");
	const [croppedImageDatasrc, setcroppedImageDatasrc] = useState('');
	const [cropenable, setCropEnable] = useState(false);
    const handleUpload = (e) => {
		e.preventDefault();
		const fileInput = document.getElementById('fileInput');
		fileInput.click();

	};

	const handleFileChange = (e) => {
		setcroppedImageDatasrc('');
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
            };
		};

		try {
			reader.readAsDataURL(file);
		} catch (error) {
			console.error(error);
		}
		
	};

	const handleCrop = () => {
		const croppedImageData = cropperRef.current.cropper.getCroppedCanvas().toDataURL();
		
		setcroppedImageDatasrc(croppedImageData);
		setHeadimage(croppedImageData);
		setCropEnable(false);
		
	};
	const uploadImage = async () =>{
		const access_token = localStorage.getItem('access_token');
		try {
			const response = await fetch("http://127.0.0.1:8000/ifm/api/reMeishi", {
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
        
    },[]);
    
    // const headImageUpload = async (e) =>{
    //     const file = e.target.files[0];
    //     const reader = new FileReader();
    //     if (file) {
    //         // 檢查文件大小（以字節為單位）
    //         const maxSizeInBytes = 25 * 1024 * 1024; // 25MB
    //         if (file.size <= maxSizeInBytes) {
    //             const regex = /\.[^.]+$/;
    //             const filenameExtension = file.name.match(regex);
    //             const allowFileType = ['.jpg', '.jpeg', '.png', '.gif', ];
                
    //             if(filenameExtension && allowFileType.includes(filenameExtension[0])){
    //                 console.log('允許', filenameExtension, file.name);
    //                 setImageName(file.name);
    //                 reader.onload = (Event) => {
    //                     const Base64Data = Event.target.result;
    //                     setHeadimage(Base64Data);
    //                 }
    //             } else {
    //                 e.target.value = '';
    //                 e.preventDefault();
    //                 console.log('不符合規範的副檔名', filenameExtension, filenameExtension[0]);
    //                 alert('不符合規範的副檔名');
    //                 return;
    //             }
                
    //         } else {
    //           alert('選擇的文件太大，請選擇小於1MB的文件。');
    //           e.target.value = ''; // 清除文件輸入字段中的值
    //         }
    //     }
        
    //     reader.readAsDataURL(file);
    // }

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
            const response = await fetch("http://127.0.0.1:8000/ifm/api/reMeishi",{
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
            <Head><title>修改個人資料</title></Head>
            <LoginState
                profilePath="./"
                resetPasswordPath="../reg/resetpassword"
                logoutPath="../uchi"
            />
            <label>頭像</label>
            <div className='cut'>
                <input
                        type="file"
                        id="fileInput"
                        accept="image/*"
                        onChange={handleFileChange}
                        style={{ display: 'none' }}
                    />
                    <button onClick={handleUpload}>上傳圖像</button>
                    {!croppedImageDatasrc && <Cropper
                        ref={cropperRef}
                        className={Style.test}
                        style={{height:100, width:'50%'}}
                        // height={originImageHeigth}
                        // width={originImageWidth}
                        aspectRatio={1}
                        zoomable={false}
                    />
                    }
                    {cropenable && <button onClick={handleCrop}>裁剪</button>}
                    
                    {croppedImageDatasrc && 
                        <>
                            <div className={Style.imagecontainer}>
                                <img 
                                    alt='裁圖'
                                    src={croppedImageDatasrc}
                                    className={Style.image}
                                />
                                
                            </div> 
                            <button onClick={uploadImage}>確定修改大頭貼</button>
                    </>}
            </div>
            <label>暱稱</label>
            <input
                type="text"
                id="username"
                name="username"
                required
                value={username}
                onChange={(e)=>setUsername(e.target.value)}
            />
            <br/>
            <label>個人簡介</label>
            <textarea
                id="describe"
                name="describe"
                required
                value={describe}
                onChange={(e)=>setDescribe(e.target.value)}
            />
            <br/>
            <label>生日</label>
            <input
                type="date"
                name="birthday"
                value={birthday}
                onChange={(e)=>setBirthday(e.target.value)}
            />

            <button
                onClick={uploadButtonClick}
            >
                修改資料
            </button>
        </>
    );
}