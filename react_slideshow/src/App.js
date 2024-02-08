import axios from "axios";
import React, { useEffect, useState } from 'react';
import {
  HashRouter as Router,
  Route,
  Routes,
  useParams,
  useSearchParams,
} from 'react-router-dom';
import Slideshow from './Slideshow';

const SlideshowWrapper = ({ interval }) => {
  const [story, setStory] = useState({});
  const { userId = 'rj' } = useParams();  // Default userId if not provided

  useEffect(() => {
    const latestStoryUrl = `/${userId}/latest_story.json`;

    axios.get(latestStoryUrl).then(response => {
      const storyUrls = response.data;
      if (storyUrls.length > 0) {
        axios.get(`/${storyUrls[0]}`).then(response => {
          setStory(response.data);
        });
      }
    });
  }, [userId]);

  return <Slideshow story={story} interval={interval} />;
};

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/slideshow/:userId" element={<SlideshowPage />} />
        <Route path="/" element={<SlideshowPage />} /> {/* Route without userId */}
      </Routes>
    </Router>
  );
};

const SlideshowPage = () => {
  // Use useSearchParams hook to access query parameters
  const [ searchParams ] = useSearchParams();
  // Get the interval from query parameters or default to 20 seconds
  const interval = parseInt(searchParams.get('interval')) || 20;

  return <SlideshowWrapper interval={interval} />;
};

export default App;
