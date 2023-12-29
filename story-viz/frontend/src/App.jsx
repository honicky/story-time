import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { HashRouter as Router, Routes, Route, useParams } from 'react-router-dom';
import Metadata from './Metadata';
import Pages from './Pages';
import { fetchSelectionsData, fetchStoryData } from './api';
import { ErrorProvider, useError } from './ErrorContext';

import ErrorMessage from './ErrorMessage';

const Story = () => {
  const [data, setData] = useState(null);
  const [selections, setSelections] = useState(null);
  const { storyId } = useParams();
  const storyUrl = `https://81rq7.apps.beam.cloud/story/${storyId}`;

  const { setError } = useError();

  useEffect(() => {
    if (storyId) {
        Promise.all([
          fetchStoryData(storyId),
          fetchSelectionsData(storyId),
        ]).then(([storyData, selectionsData]) => {
          setData(storyData);
          setSelections(selectionsData);
        }).catch((error) => {
          setError(`Error fetching story or selection: ${error}`);
        });
    } else {
      setError('storyId not provided');
    }
  }, [storyId]);

  if (!data || selections === null) {
    return <div>Loading...</div>;
  }

  return (
    <div>
        <ErrorMessage />
        <Metadata data={data} storyUrl={storyUrl} />
        <Pages pages={data.pages} selections={selections} storyId={storyId} />
    </div>
  );
};

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/:storyId?" element={<ErrorProvider><Story /></ErrorProvider>} />
      </Routes>
    </Router>
  );
};

export default App;
