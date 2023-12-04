// App.js
import React, { useState, useEffect } from 'react';
import queryString from 'query-string';
import Metadata from './Metadata';
import Pages from './Pages';

const App = () => {
  const [data, setData] = useState(null);
  const queryParams = queryString.parse(window.location.search);
  const jsonUrl = queryParams.jsonUrl;

  useEffect(() => {
    if (jsonUrl) {
      fetch(jsonUrl)
        .then(response => response.json())
        .then(data => setData(data))
        .catch(error => console.error('Error fetching JSON:', error));
    } else {
      console.error('JSON URL not provided');
    }
  }, [jsonUrl]);

  if (!data) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <Metadata data={data} jsonUrl={jsonUrl} />
      <Pages pages={data.pages} />
    </div>
  );
};

export default App;
