import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { HashRouter as Router, Routes, Route, useParams } from 'react-router-dom';
import Metadata from './Metadata';
import Pages from './Pages';

import { ErrorProvider } from './ErrorContext';
import ErrorMessage from './ErrorMessage';

const Story = () => {
  const [data, setData] = useState(null);
  const [selections, setSelections] = useState(null);
  const { storyId } = useParams();
  const storyUrl = `https://81rq7.apps.beam.cloud/story/${storyId}`;
  const selectionsUrl = `https://81rq7.apps.beam.cloud/story/${storyId}/selections`;
  const authorizationHeader = import.meta.env.VITE_AUTHORIZATION;

  const fetchStoryData = async () => {
    try {
      const response = await axios.get(storyUrl, {
        headers: {"Authorization": `Basic ${authorizationHeader}`},
        referrerPolicy: "origin",
      });
      setData(response.data);
    } catch (error) {
      console.error('Error fetching story:', error);
    }
  };

  const fetchSelectionsData = async () => {
    try {
      const response = await axios.get(selectionsUrl, {
        headers: {"Authorization": `Basic ${authorizationHeader}`},
        referrerPolicy: "origin",
      });
      setSelections(response.data);
    } catch (error) {
      if (error.response && error.response.status === 404) {
        setSelections([]); // Set selections to an empty array if 404
      } else {
        console.error('Error fetching selections:', error);
      }
    }
  };

  useEffect(() => {
    if (storyId) {
      fetchStoryData();
      fetchSelectionsData();
    } else {
      console.error('storyId not provided');
    }
  }, [storyUrl, selectionsUrl, storyId]);

  if (!data || selections === null) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <ErrorProvider>
        <ErrorMessage />

        <Metadata data={data} storyUrl={storyUrl} />
        <Pages pages={data.pages} selections={selections} storyId={storyId} />
        </ErrorProvider>
    </div>
  );
};

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/:storyId" element={<Story />} />
      </Routes>
    </Router>
  );
};

export default App;
