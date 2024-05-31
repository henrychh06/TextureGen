import React from 'react';

interface NormalMapDisplayProps {
  normalMapUrl: string;
  roughnessMapUrl: string;
  displacementMapUrl: string;
}

const NormalMapDisplay: React.FC<NormalMapDisplayProps> = ({ normalMapUrl, roughnessMapUrl, displacementMapUrl }) => {
  if (!normalMapUrl && !roughnessMapUrl && !displacementMapUrl) return null;

  return (
    <div className="mt-4 grid grid-cols-3 gap-4">
      {normalMapUrl && <img src={normalMapUrl} alt="Normal Map" className="border rounded" />}
      {roughnessMapUrl && <img src={roughnessMapUrl} alt="Roughness Map" className="border rounded" />}
      {displacementMapUrl && <img src={displacementMapUrl} alt="Displacement Map" className="border rounded" />}
    </div>
  );
};

export default NormalMapDisplay;
