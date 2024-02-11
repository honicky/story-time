import React, { useState, useEffect } from 'react';
import styles from './ImageCarousel.module.css';

const ImageCarousel = ({ images, selectedIndex, onSelect }) => {
  const [offset, setOffset] = useState(0);

  // Ensure the selected index is visible initially
  useEffect(() => {
    setOffset(Math.floor((selectedIndex ? selectedIndex : 0) / 4) * 4);
  }, [selectedIndex]);

  const scrollLeft = () => {
    setOffset(Math.max(0, offset - 4));
  };

  const scrollRight = () => {
    setOffset(Math.min(images.length - 4, offset + 4)); // Assumes at least 4 images are always displayed
  };

  return (
    <div className={styles.carouselContainer}>
      {offset > 0 && (
        <button onClick={scrollLeft} className={`${styles.arrowButton} ${styles.leftArrow}`}>
          {"<"}
        </button>
      )}

      <div className={styles.imagesContainer}>
        {images.slice(offset, offset + 5).map((imageUrl, index) => (
          <div key={index} className={`${styles.imageWrapper} ${index + offset === selectedIndex ? styles.selectedImage : ''}`}>
            <img
              src={imageUrl}
              alt={`Image ${index + 1}`}
              onClick={() => onSelect(index + offset)}
              className={styles.carouselImage}
            />
          </div>
        ))}
      </div>

      {offset < images.length - 4 && (
        <button onClick={scrollRight} className={`${styles.arrowButton} ${styles.rightArrow}`}>
          {">"}
        </button>
      )}
    </div>
  );
};

export default ImageCarousel;
