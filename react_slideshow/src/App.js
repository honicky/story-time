import axios from "axios";
import React, { useEffect, useState } from 'react';
import {
  HashRouter,
  Route,
  Routes,
  useLocation,
} from 'react-router-dom';
import Slideshow from './Slideshow';

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

// const SlideshowWrapper = ({ jsonUrl, interval }) => {
//   const [pages, setPages] = useState([]);

//   useEffect(() => {
//     if (jsonUrl) {
//       axios.get(jsonUrl).then((response) => {
//         setPages(response.data.pages);
//       });
//     }
//   }, [jsonUrl]);

//   return <Slideshow pages={pages} interval={interval} />;
// };


const SlideshowWrapper = () => {
  const [story, setStory] = useState({});
  const [storyUrl, setStoryUrl] = useState('');
  const [interval, setInterval] = useState(5);
  const query = useQuery();

  useEffect(() => {
    const storyUrlParam = query.get('story_url');
    if (storyUrlParam) {
      setStoryUrl(storyUrlParam);
    }

    const intervalParam = query.get('interval');
    if (intervalParam) {
      setInterval(parseInt(intervalParam));
    }
  }, [query]);

  useEffect(() => {
    if (storyUrl) {
      axios.get(storyUrl).then((response) => {
        setStory(response.data);
      });
    }
  }, [storyUrl]);

  return <Slideshow story={story} interval={interval} />;
};

const App = () => {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<SlideshowPage />} />
      </Routes>
    </HashRouter>
  );
};

const SlideshowPage = () => {
  const location = useLocation();
  const query = new URLSearchParams(location.search);

  const jsonUrl = query.get('jsonUrl');
  const interval = parseInt(query.get('interval')) || 5; // Default to 5 seconds

  return <SlideshowWrapper jsonUrl={jsonUrl} interval={interval} />;
};

export default App;

