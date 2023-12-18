import React from 'react';
import { useError } from './ErrorContext';
import styles from './ErrorMessage.module.css'; // Style as needed

const ErrorMessage = () => {
  const { error } = useError();

  if (!error) return null;

  return <div className={styles.errorContainer}>{error}</div>;
};

export default ErrorMessage;