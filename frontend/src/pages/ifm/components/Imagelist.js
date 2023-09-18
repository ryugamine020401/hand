import React from 'react';
import Image from 'next/image';


function ImageList({ urlArray }) {
  return (
    <div>
      {urlArray.map((url, index) => (
        <Image key={index} src={url} alt={`Image ${index}`} />
      ))}
    </div>
  );
}

export default ImageList;