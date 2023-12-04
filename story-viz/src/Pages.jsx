import React, { useState } from 'react';

const Pages = ({ pages }) => {
  const [selectedImages, setSelectedImages] = useState({});

  const handleImageSelect = (pageIndex, imageUrl) => {
    setSelectedImages({ ...selectedImages, [pageIndex]: imageUrl });
  };

  const imageHeight = window.innerHeight / 3

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '10px' }}>
      {pages.map((page, pageIndex) => (
        <div key={pageIndex} style={{ border: '1px solid white', padding: '10px', marginBottom: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            {page.image_urls.map((imageUrl, imageIndex) => (
              <div key={imageIndex} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '0 10px' }}>
                <img 
                  src={imageUrl}
                  alt={`Page ${pageIndex + 1} Image ${imageIndex + 1}`}
                  style={{
                    height: imageHeight,
                    maxWidth: '100%',
                    border: selectedImages[pageIndex] === imageUrl ? '3px solid blue' : 'none',
                    cursor: 'pointer',
                    marginBottom: '10px'
                  }}
                  onClick={() => handleImageSelect(pageIndex, imageUrl)}
                />
                <button onClick={() => handleImageSelect(pageIndex, imageUrl)}>Select</button>
              </div>
            ))}
          </div>
          <div>
            <p>{page.paragraph}</p>
            <p><em>{page.image_prompt}</em></p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Pages;
