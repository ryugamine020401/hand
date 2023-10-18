import style from '@/pages/study/css/uploadteachimage.module.css';
import { useState } from 'react';
import LoginState from '@/components/loginstate';
import Image from 'next/image';

export default function UploadTeachImage() {
    const backendurl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const [describe, setDescribe] = useState('');
    const [img, setBase64img] = useState();
    console.log("載入");

    const handleImageUpload = (e) => {
        const file = e.target.files[0]; // 獲取選擇的文件
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const base64Image = event.target.result; // 獲取Base64圖像數據
                setBase64img(base64Image);
                console.log("Base64圖像：", base64Image);
                console.log("描述",describe);
            };
            reader.readAsDataURL(file); // 開始讀取文件並觸發onload事件
        }
    };

    const uploadimagebuttonclick = async () => {
        if (describe === '') {
            window.alert('請出入影像描述');
            return;
        } else {
            
        }
        const response = await fetch(`${backendurl}/study/api/uploadimg`, {
            method:'POST',
            body:JSON.stringify({img, describe}),
            headers:{
                'Authorization':`Bearer FSSDF`,
                'Content-Type':'application/json',
            }
        });
        try {
            if (response.status === 200) {
                const responseData = await response.json();
                console.log(responseData.message);
            } else {
                const responseData = await response.json();
                console.log(responseData.message);
            }
        } catch (error) {
           console.error(error);
        }
    }

    

    return (
        <div className={style.pagecontianer}>
            <LoginState
                    profilePath="../ifm"
                    resetPasswordPath="./reg/resetpassword"
                    logoutPath="./uchi"
            />
            <div className={style.fromcontainer}>
                <div className={style.uppercontianer}>
                    <div className={style.leftcontainer}>
                        <label htmlFor="imageUpload">選擇圖片：</label>
                        <input type="file" accept="image/*" onChange={handleImageUpload} />
                    </div>
                    {img &&
                        <div className={style.rightcontainer}>
                            <Image
                                alt='root傳的圖片預覽'
                                height={200}
                                width={200}
                                src={img}
                            />
                        </div>
                    }
                </div>
                
                <div className={style.lowercontianer}>
                    <textarea placeholder='教學圖片描述' onChange={(e) => setDescribe(e.target.value)}></textarea>
                    <button onClick={uploadimagebuttonclick}>上傳圖片</button>
                </div>
               
            </div>
        </div>
    );
}
