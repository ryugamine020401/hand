import React, { useRef, useState } from 'react';
import Cropper from 'react-cropper';
import 'cropperjs/dist/cropper.css';

export default function CropPage() {
  const cropperRef = useRef(null);
  // const imageRef = useRef(null);

  const [croppedImageDatasrc, setcroppedImageDatasrc] = useState('');
  const [originImageWidth, setOriginImageWidth] = useState(0);
  const [originImageHeigth, setOriginImageHeigth] = useState(0);

  const handleUpload = (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('fileInput');
    fileInput.click();
  };

  const handleFileChange = (e) => {
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
        setOriginImageWidth(img.width);
        setOriginImageHeigth(img.height);
      };
    };

    reader.readAsDataURL(file);
  };

  const handleCrop = () => {
    const croppedImageData = cropperRef.current.cropper.getCroppedCanvas().toDataURL();
    // 此處您可以將裁剪後的圖像數據上傳到後端或執行其他操作
    console.log(croppedImageData);
    setcroppedImageDatasrc(croppedImageData);
  };

  return (
    <div>
      <input
        type="file"
        id="fileInput"
        accept="image/*"
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
      <button onClick={handleUpload}>上傳圖像</button>
      <Cropper
        ref={cropperRef}
        // style={{ height: 400, width: '100%' }}
        style={{ width: '100%' }}
        // height={originImageHeigth}
        // width={originImageWidth}
        aspectRatio={1}
        zoomable={false}
      />
      <button onClick={handleCrop}>裁剪</button>
      {croppedImageDatasrc && <img
                        alt='裁圖'
                        src={croppedImageDatasrc}
                        /> }
    </div>
    
  );
};
