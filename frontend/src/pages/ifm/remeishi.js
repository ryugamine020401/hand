import LoginState from "@/components/loginstate";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";


export default function ReMeishi(){
    const router = useRouter();
    const [username, setUsername] = useState("");
    const [describe, setDescribe] = useState("");
    const [birthday, setBirthday] = useState("");
    const [headimage, setHeadimage] = useState("");
    const [imageName, setImageName] = useState("");

    
    useEffect(()=>{
        const access_token = localStorage.getItem('access_token');
        if (access_token === null){
            router.push('../uchi');
        }
        console.log(access_token);
        
    },[]);
    
    const headImageUpload = async (e) =>{
        const file = e.target.files[0];
        const reader = new FileReader();
        if (file) {
            // 檢查文件大小（以字節為單位）
            const maxSizeInBytes = 25 * 1024 * 1024; // 25MB
            if (file.size <= maxSizeInBytes) {
                const regex = /\.[^.]+$/;
                const filenameExtension = file.name.match(regex);
                const allowFileType = ['.jpg', '.jpeg', '.png', '.gif', ];
                
                if(filenameExtension && allowFileType.includes(filenameExtension[0])){
                    console.log('允許', filenameExtension, file.name);
                    setImageName(file.name);
                    reader.onload = (Event) => {
                        const Base64Data = Event.target.result;
                        setHeadimage(Base64Data);
                    }
                } else {
                    e.target.value = '';
                    e.preventDefault();
                    console.log('不符合規範的副檔名', filenameExtension, filenameExtension[0]);
                    alert('不符合規範的副檔名');
                    return;
                }
                
            } else {
              alert('選擇的文件太大，請選擇小於1MB的文件。');
              e.target.value = ''; // 清除文件輸入字段中的值
            }
        }
        
        reader.readAsDataURL(file);
    }

    const uploadButtonClick = async () =>{

        if(username != "" && birthday != "" && describe != "" && headimage != ""){
            console.log("都有東西");
        } else {
            alert('欄位不得為空')
            console.log("沒有足夠的東西");
            return;
        }

        console.log(imageName);

        try {
            const access_token = localStorage.getItem('access_token');
            const response = await fetch("http://127.0.0.1:8000/ifm/reMeishi",{
                method:"POST",
                body:JSON.stringify({username, birthday, describe, headimage, imageName,}),
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
            <label>頭像</label>
            <input 
                type="file" 
                name="fileInput"
                
                onChange={headImageUpload}
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