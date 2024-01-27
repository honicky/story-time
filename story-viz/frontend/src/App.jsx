import React, { useState, useEffect } from 'react';
import { HashRouter as Router, Routes, Route, useParams } from 'react-router-dom';
import Login from './Login'
import Metadata from './Metadata';
import Pages from './Pages';
import StoryList from './StoryList';
import { fetchSelectionsData, fetchStoryData } from './api';
import { useError } from './ErrorContext';
import { useToken } from './TokenContext';
import ErrorMessage from './ErrorMessage';

const Story = () => {
  const [data, setData] = useState(null);
  const [selections, setSelections] = useState(null);
  const { storyId } = useParams();
  const storyUrl = `https://81rq7.apps.beam.cloud/story/${storyId}`;

  const { setError } = useError();
  const { token } = useToken();

  useEffect(() => {
    if (storyId) {
        Promise.all([
          fetchStoryData(storyId, token),
          fetchSelectionsData(storyId, token),
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

  const { token } = useToken();

  // TODO: handle expired tokens
  if(!token) {
    return (
        <Login />
    )
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={
            <StoryList />
        } />
        <Route path="/story/:storyId" element={
            <Story />
        } />
      </Routes>
    </Router>
  );
};

export default App;
