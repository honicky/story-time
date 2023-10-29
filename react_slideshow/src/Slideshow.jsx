import React, { useState, useEffect } from "react";

const Slideshow = ({ images, sentences }) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setCurrentIndex((currentIndex + 1) % images.length);
    }, 5000);
    return () => clearInterval(intervalId);
  }, [currentIndex, images]);

  return (
    <div style={{ height: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <img alt={sentences[currentIndex]} src={images[currentIndex]} style={{ maxHeight: "100%", maxWidth: "100%" }} />
    </div>
  );
};

export default Slideshow;