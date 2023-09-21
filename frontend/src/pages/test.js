import { useState, createRef } from 'react';
import Cropper from 'react-cropper';
import 'cropperjs/dist/cropper.css';

const CropperPage = () => {
  const [image, setImage] = useState(null);
  const [croppedImage, setCroppedImage] = useState(null);
  const cropperRef = createRef();

  const handleImageChange = (e) => {
    e.preventDefault();
    const files = e.target.files[0];
    // if (e.dataTransfer) {
    //     files = e.dataTransfer.files;
    //   } else if (e.target) {
    //     files = e.target.files;
    // }
    const reader = new FileReader();

    reader.onload = (e) => {
      setImage(e.target.result);
    };

    if (files) {
      reader.readAsDataURL(files);
    }
  };

  const handleCrop = () => {
    if (cropperRef.current) {
        cropperRef.current.getCroppedCanvas().toBlob((blob) => {
        const croppedImageUrl = URL.createObjectURL(blob);
        setCroppedImage(croppedImageUrl);
      });
    }
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleImageChange} />
      {image && (
        <div>
          <ReactCropper
                ref={cropperRef} // 设置 cropperRef
                src={image}
                style={{ height: 300, width: '100%' }}
                aspectRatio={1}
                guides={true}
            />
          <button onClick={handleCrop}>裁剪图像</button>
        </div>
      )}
      {croppedImage && (
        <div>
          <h2>裁剪后的图像：</h2>
          <img src={croppedImage} alt="Cropped" />
        </div>
      )}
    </div>
  );
};

export default CropperPage;
