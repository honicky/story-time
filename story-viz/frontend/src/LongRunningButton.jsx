import React, { useState } from 'react';
import styles from './LongRunningButton.module.css';

// Takes an async function `asyncAction` as a prop
const LongRunningButton = ({ onClick, className, children }) => {
  const [isLoading, setIsLoading] = useState(false);

  const handleButtonClick = async () => {
    setIsLoading(true);
    try {
      if (onClick) { await onClick(); }
    } finally {
      setIsLoading(false); // Stop loading regardless of success or failure
    }
  };

  return (
    <button onClick={handleButtonClick} disabled={isLoading} className={className}>
      {isLoading && <span className={styles.spinner}></span>}
      {children}
    </button>
  );
};

export default LongRunningButton;
