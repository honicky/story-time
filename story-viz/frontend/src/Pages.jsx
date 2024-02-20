import React, { useState, useEffect } from 'react';
import ImageCarousel from './ImageCarousel';
import LongRunningButton from './LongRunningButton';
import { postSelections, putImagePrompt } from './api';
import styles from './Pages.module.css';
import { useError } from './ErrorContext';
import { useToken } from './TokenContext';
import { useNavigate } from 'react-router-dom';

const Pages = ({ pages, selections, storyId, handleGenerateImages }) => {
  const [selectedImages, setSelectedImages] = useState([]);
  const [editablePrompts, setEditablePrompts] = useState({});
  const [hasEdited, setHasEdited] = useState({});

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
    // Initialize editable prompts
    const initialPrompts = pages.reduce((acc, page, index) => {
      acc[index] = page.image_prompt[page.image_prompt.length - 1] || '';
      return acc;
    }, {});
    setEditablePrompts(initialPrompts);
    setHasEdited({});
  }, [pages, selections, setError]);

  const handleImageSelect = (pageIndex, imageIndex) => {
    const newSelectedImages = [...selectedImages];
    newSelectedImages[pageIndex] = imageIndex;
    setSelectedImages(newSelectedImages);
    setError('');
  };

  const handlePromptChange = (pageIndex, newValue) => {
    setEditablePrompts(prev => ({ ...prev, [pageIndex]: newValue }));
    setHasEdited(prev => ({ ...prev, [pageIndex]: true }));
  };

  const saveImagePrompt = async (pageIndex) => {
    if (!hasEdited[pageIndex]) return; // Only save if edited
    setError('');
    try {
      // Placeholder for save logic; replace with your actual API call
      console.log('Saving prompt for page', pageIndex, ':', editablePrompts[pageIndex]);
      await putImagePrompt(storyId, pageIndex, editablePrompts[pageIndex], token);
      setHasEdited(prev => ({ ...prev, [pageIndex]: false })); // Reset edited state after saving
    } catch (error) {
      setError('Error saving image prompt:', error);
    }
  };

  const handleGenerateImagesWithSave = async (pageIndex) => {
    try {
      await saveImagePrompt(pageIndex);
      await handleGenerateImages(pageIndex);
    } catch (error) {
      setError('Error generating images:', error);
    }
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
            <p className={styles.pageText}>{page.paragraph[page.paragraph.length - 1]}</p>
            <div className={styles.editablePromptContainer}>
              <textarea
                className={styles.editablePrompt}
                value={editablePrompts[pageIndex]}
                onChange={(e) => handlePromptChange(pageIndex, e.target.value)}
              />
              <button
                className={styles.saveButton}
                disabled={!hasEdited[pageIndex]}
                onClick={() => saveImagePrompt(pageIndex)}
              >
                Save Image Prompt
              </button>
            </div>
          </div>
          <LongRunningButton 
            className={styles.submitButton} 
            onClick={() => handleGenerateImagesWithSave(pageIndex)}
          >
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
