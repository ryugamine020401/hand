import React, { useRef, useState } from 'react';
import Cropper from 'react-cropper';
import 'cropperjs/dist/cropper.css';
import Style from './crop.module.css'

export default function CropPage() {
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

	const handleCrop = () => {
		const croppedImageData = cropperRef.current.cropper.getCroppedCanvas().toDataURL();
		
		setcroppedImageDatasrc(croppedImageData);
		setHeadimage(croppedImageData);
		setCropEnable(false);
		// console.log(croppedImageData);
		
	};
	const uploadImage = async () =>{
		const access_token = localStorage.getItem('access_token');
		try {
			// setHeadimage(croppedImageDatasrc);
			// console.log(croppedImageDatasrc);
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

  return (
	<>
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
	</>
    
  );
};

