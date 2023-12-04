// Metadata.js
import React from 'react';

const Metadata = ({ data, jsonUrl }) => {
  return (
    <div style={{ padding: '10px', border: '1px solid #ccc', marginBottom: '20px' }}>
      <h2>Story Outline</h2>
      {Object.entries(data.outline).map(([key, value]) => (
        <div key={key} style={{ marginBottom: '10px' }}>
          <h3 style={{ margin: '5px 0' }}>{key}</h3>
          {typeof value === 'object' ? (
            Object.entries(value).map(([subKey, subValue]) => (
              <p key={subKey} style={{ margin: '2px 0' }}><strong>{subKey}:</strong> {subValue}</p>
            ))
          ) : (
            <p style={{ margin: '2px 0' }}>{value}</p>
          )}
        </div>
      ))}
      {jsonUrl && <a href={jsonUrl} target="_blank" rel="noopener noreferrer">View JSON File</a>}
    </div>
  );
};

export default Metadata;
