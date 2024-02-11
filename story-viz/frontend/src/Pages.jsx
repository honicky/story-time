import ImageCarousel from './ImageCarousel';
import LongRunningButton from './LongRunningButton';
import { postSelections,  } from './api';
import React, { useState, useEffect } from 'react';
import styles from './Pages.module.css';
import { useError } from './ErrorContext';
import { useToken } from './TokenContext';
import { useNavigate } from 'react-router-dom';

const Pages = ({ pages, selections, storyId, handleGenereateImages }) => {
  const [selectedImages, setSelectedImages] = useState([]);

  const { setError } = useError();
  const { token } = useToken();
  const navigate = useNavigate();

  useEffect(() => {
    if (selections && selections.length > 0) {
      setSelectedImages(selections[selections.length - 1].selections);
    } else {
      setSelectedImages([]);
    }
    setError('');
  }, [selections, setError]);

  const handleImageSelect = (pageIndex, imageIndex) => {
    const newSelectedImages = [...selectedImages];
    newSelectedImages[pageIndex] = imageIndex;
    setSelectedImages(newSelectedImages);
    setError('');
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
      await postSelections(storyId, selectedImages, token);
      navigate("/");
    } catch (error) {
      setError('Error posting selections:', error);
    }
  };

  return (
    <div className={styles.pagesContainer}>
      {pages.map((page, pageIndex) => (
        <div key={pageIndex} className={styles.pageContainer}>
          <ImageCarousel
            images={page.image_urls}
            selectedIndex={selectedImages[pageIndex]}
            onSelect={index => handleImageSelect(pageIndex, index)}
          />
          <div>
            <p className={styles.pageText}>{page.paragraph}</p>
            <p className={styles.pageText}><em>{page.image_prompt}</em></p>
          </div>
          <LongRunningButton className={styles.submitButton} onClick={() => handleGenereateImages(pageIndex)}>
            Generate More Images
          </LongRunningButton>
        </div>
      ))}
      <button className={styles.submitButton} onClick={handleSubmitSelections}>
        Submit Selections
      </button>
    </div>
  );
};

export default Pages;
