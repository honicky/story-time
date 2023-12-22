import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './Pages.module.css';
import { useError } from './ErrorContext';
import { postSelections } from './api';

const Pages = ({ pages, selections, storyId }) => {
  const [selectedImages, setSelectedImages] = useState([]);

  const { setError } = useError();

  useEffect(() => {
    if (selections && selections.length > 0) {
      setSelectedImages(selections[selections.length - 1].selections);
    } else {
      setSelectedImages([]);
    }
    setError('')
  }, [pages, selections]);

  const handleImageSelect = (pageIndex, imageIndex) => {
    const newSelectedImages = [...selectedImages];
    newSelectedImages[pageIndex] = imageIndex;
    setSelectedImages(newSelectedImages);
    setError('')
  };

  const handleSubmitSelections = async () => {
    const isPayloadValid = selectedImages.length === pages.length &&
                           selectedImages.every((imageIndex, pageIndex) => 
                             Number.isInteger(imageIndex) &&
                             imageIndex >= 0 &&
                             imageIndex < pages[pageIndex].image_urls.length
                           );
  
    if (!isPayloadValid) {
      setError('Invalid payload: Each selection must be a valid integer within the range of image URLs for its respective page.');
      return;
    }
    try {
      await postSelections(storyId, selectedImages);
    } catch (error) {
      setError('Error posting selections:', error);
    }
  };

  return (
    <div className={styles.pagesContainer}>
      {pages.map((page, pageIndex) => (
        <div key={pageIndex} className={styles.pageContainer}>
          <div className={styles.imageContainer}>
            {page.image_urls.map((imageUrl, imageIndex) => (
              <div key={imageIndex} className={styles.imageWrapper}>
                <img 
                  src={imageUrl}
                  alt={`Page ${pageIndex + 1} Image ${imageIndex + 1}`}
                  className={`${styles.image} ${selectedImages[pageIndex] === imageIndex ? styles.selectedImage : styles.unselectedImage}`}
                  onClick={() => handleImageSelect(pageIndex, imageIndex)}
                />
              </div>
            ))}
          </div>
          <div>
            <p className={styles.pageText}>{page.paragraph}</p>
            <p className={styles.pageText}><em>{page.image_prompt}</em></p>
          </div>
        </div>
      ))}
      <button className={styles.submitButton} onClick={handleSubmitSelections}>
        Submit Selections
      </button>
    </div>
  );
};

export default Pages;
