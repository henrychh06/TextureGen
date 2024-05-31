import React from 'react';

interface ImageDisplayProps {
  imageUrl: string;
}

const ImageDisplay: React.FC<ImageDisplayProps> = ({ imageUrl }) => {
  if (!imageUrl) return null;

  return (
    <div className="flex justify-center mt-4">
      <img src={imageUrl} alt="Generated" className="border rounded" />
    </div>
  );
};

export default ImageDisplay;
