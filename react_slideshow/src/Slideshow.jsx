import React, { useState, useEffect } from "react";
import styles from './Slideshow.module.css';

console.log(styles)

const Slideshow = ({ story, interval }) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (!story || !story.pages || story.pages.length === 0 ) return;

    const intervalId = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % story.pages.length);
    }, interval * 1000);
    
    return () => clearInterval(intervalId);
  }, [currentIndex, story, interval]);

  if (! story || ! story.pages || story.pages.length === 0 ) {
    return <div>No pages in story</div>;
  }

  return (
    <div className={styles['slideshow-container']}>
      <div className={styles['image-container']}>
        <img
          alt={story.pages[currentIndex].text}
          src={story.pages[currentIndex].image_url}
        />
      </div>
      <div className={styles['text-container']}>
        <p>{story.pages[currentIndex].text}</p>
      </div>
    </div>
  );
};

export default Slideshow;
