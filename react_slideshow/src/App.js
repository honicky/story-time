import axios from "axios";
import React, { useEffect, useState } from 'react';
import {
  HashRouter as Router,
  Route,
  Routes,
  useParams,
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
  const interval = 20; // Default to 20 seconds, or get it from query if needed

  return <SlideshowWrapper interval={interval} />;
};

export default App;
