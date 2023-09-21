import React, { useRef, useState } from 'react';
import Cropper from 'react-cropper';
import 'cropperjs/dist/cropper.css';
import Style from './crop.module.css'

export default function CropPage() {
  const cropperRef = useRef(null);
  const [headimage, setHeadimage] = useState("");
  // const imageRef = useRef(null);

  const [croppedImageDatasrc, setcroppedImageDatasrc] = useState('');
//   const [originImageWidth, setOriginImageWidth] = useState(0);
//   const [originImageHeigth, setOriginImageHeigth] = useState(0);
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
        // setOriginImageWidth(img.width);
        // setOriginImageHeigth(img.height);
      };
    };
    try {
        reader.readAsDataURL(file);
    } catch (error) {
        console.error(error);
    }
    
  };

  const handleCrop = async () => {
    const croppedImageData = await cropperRef.current.cropper.getCroppedCanvas().toDataURL();
    const access_token = await localStorage.getItem('access_token');
    setHeadimage(croppedImageData);
    // console.log(cropperRef.current.cropper.getCroppedCanvas().toDataURL());
    console.log(headimage);
    try {
        const response = await fetch("http://127.0.0.1:8000/ifm/reMeishi", {
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
    // console.log(croppedImageData);
    setcroppedImageDatasrc(croppedImageData);
    setCropEnable(false);
  };

  return (
    <div>
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
        style={{ height: 400, width: '100%' }}
        // height={originImageHeigth}
        // width={originImageWidth}
        aspectRatio={1}
        zoomable={false}
      />
      }
      {cropenable && <button onClick={handleCrop}>裁剪</button>}
       
      {croppedImageDatasrc && 
        <div className={Style.imagecontainer}>
            <img 
                alt='裁圖'
                src={croppedImageDatasrc}
                className={Style.image}
            />
        </div>
                 }
    </div>
    
  );
};

