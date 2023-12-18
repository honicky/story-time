import React, { useState, useEffect } from "react";

const Slideshow = ({ story, interval }) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const pages = (story || {}).pages || [];

    const intervalId = setInterval(() => {
      setCurrentIndex((currentIndex + 1) % pages.length);
    }, interval * 1000); // Convert seconds to milliseconds
    return () => clearInterval(intervalId);
  }, [currentIndex, story, interval]);

  const pages = (story || {}).pages || [];
  if (pages.length === 0) {
    return <div>Story is empty</div>;
  }

  const fontSize = `${window.innerHeight / 20}px`; // 1/20th of the viewport height

  return (
    <div style={{ height: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: "50%", height: "100%", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <img alt={pages[currentIndex].paragraph} src={pages[currentIndex].image_urls[0]} style={{ maxHeight: "100%", maxWidth: "100%" }} />
      </div>
      <div style={{ width: "50%", height: "100%", display: "flex", alignItems: "center", justifyContent: "center", padding: "80px", fontFamily: "'Karla', sans-serif", fontSize: fontSize, color: "#444444", lineHeight: 1.6 }}>
        <p>{pages[currentIndex].paragraph}</p>
      </div>
    </div>
  );
};

export default Slideshow;
