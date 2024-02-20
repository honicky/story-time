import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useParams } from 'react-router-dom';
import Login from './Login'
import Metadata from './Metadata';
import Pages from './Pages';
import StoryList from './StoryList';
import { fetchSelectionsData, fetchStoryData, postGenerateImages } from './api';
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

  const handleGenerateImages = async (pageIndex) => {
    const isPayloadValid = Number.isInteger(pageIndex) &&
                           pageIndex >= 0 &&
                           pageIndex < data.pages.length;

    if (!isPayloadValid) {
      setError('Invalid payload: Page index must be a valid integer within the range of pages.');
      return;
    }
    try {
      await postGenerateImages(storyId, pageIndex, token);
      const storyData = await fetchStoryData(storyId, token)
      setData(storyData);
    } catch (error) {
      setError('Error generating images:', error);
    }
  }

  if (!data || selections === null) {
    return <div>Loading...</div>;
  }

  return (
    <div>
        <ErrorMessage />
        <Metadata data={data} storyUrl={storyUrl} />
        <Pages pages={data.pages} selections={selections} storyId={storyId} handleGenerateImages={handleGenerateImages}/>
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
