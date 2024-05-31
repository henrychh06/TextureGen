"use client";

import React, { useState } from "react";
import axios from "axios";
import "./styyle.css";

export default function Home() {
  const [imageUrl, setImageUrl] = useState("");
  const [normalMapUrl, setNormalMapUrl] = useState("");
  const [roughnessMapUrl, setRoughnessMapUrl] = useState("");
  const [displacementMapUrl, setDisplacementMapUrl] = useState("");
  const [prompt, setPrompt] = useState("");
  const [albedoMapUrl, setAlbedoMapUrl] = useState("");
  const [bumpMapUrl, setBumpMapUrl] = useState(""); 
  const [specularMapUrl, setSpecularMapUrl] = useState(""); 
  const [metalMapUrl, setMetalMapUrl] = useState("")
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalImageUrl, setModalImageUrl] = useState("");

  const handlePromptSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    try {
      const response = await axios.post("http://34.226.140.77/upload", {
        prompt,
      });
      const { base_image, normal_map, roughness, displacement, albedo_map, bump_map, spec_map, metal_map} = response.data;

      setImageUrl(`data:image/png;base64,${base_image}`);
      setNormalMapUrl(`data:image/png;base64,${normal_map}`);
      setRoughnessMapUrl(`data:image/png;base64,${roughness}`);
      setDisplacementMapUrl(`data:image/png;base64,${displacement}`);
      setAlbedoMapUrl(`data:image/png;base64,${albedo_map}`);
      setBumpMapUrl(`data:image/png;base64,${bump_map}`); 
      setSpecularMapUrl(`data:image/png;base64,${spec_map}`); 
      setMetalMapUrl(`data:image/png;base64,${metal_map}`);
    } catch (error) {
      console.error("Error generating image:", error);
    }
  };

  const handleImageClick = (imageUrl:string) => {
    setModalImageUrl(imageUrl);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setModalImageUrl("");
  };

  return (
    <main className="container">
      <h1 className="title">Textures</h1>
      <form onSubmit={handlePromptSubmit} className="form">
        <textarea
          className="textarea"
          placeholder="Enter your prompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <button type="submit" className="button">
          Generate
        </button>
      </form>
      {imageUrl && (
        <div className="results">
          <h2 className="subtitle">Generated Images</h2>
          <div className="images">
            <div className="image-card">
              <h3 className="image-title">Base Image</h3>
              <img src={imageUrl} alt="Base Image" className="image" />
            </div>
            <div className="image-card">
              <h3 className="image-title">Normal Map</h3>
              <img src={normalMapUrl} alt="Normal Map" className="image" />
            </div>
            <div className="image-card">
              <h3 className="image-title">Roughness Map</h3>
              <img src={roughnessMapUrl} alt="Roughness Map" className="image" />
            </div>
            <div className="image-card">
              <h3 className="image-title">Displacement Map</h3>
              <img src={displacementMapUrl} alt="Displacement Map" className="image" />
            </div>
            <div className="image-card">
              <h3 className="image-title">Specular Map</h3>
              <img src={specularMapUrl} alt="Specular Map" className="image" />
            </div>
            <div className="image-card">
              <h3 className="image-title">Bump Map</h3>
              <img src={bumpMapUrl} alt="Bump Map" className="image" />
            </div>
            <div className="image-card">
              <h3 className="image-title">Metal Map</h3>
              <img src={metalMapUrl} alt="Metal Map" className="image" />
            </div>
          </div>
        </div>
      )}

      {isModalOpen && (
        <div className="modal" onClick={handleCloseModal}>
          <div className="modal-content">
            <img src={modalImageUrl} alt="Modal" className="modal-image" />
          </div>
        </div>
      )}      

    </main>
  );
}
