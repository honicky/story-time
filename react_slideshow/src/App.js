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

const SlideshowWrapper = () => {
  const [userId, setUserId] = useState('rj-test-user'); // Default user_id
  const query = useQuery();

  const [imagePaths, setImagePaths] = useState([]);
  const [sentences, setSentences] = useState([]);

  useEffect(() => {
    const userIdParam = query.get('user_id');
    if (userIdParam) {
      setUserId(userIdParam);
    }
  }, [query]);

  useEffect(() => {
    if (userId) {
      axios.get(`/${userId}/story_descriptor.json`).then((response) => {
        setImagePaths(response.data.image_paths);
        setSentences(response.data.sentences);
      });
    }
  }, [userId]);

  return <Slideshow images={imagePaths} sentences={sentences} />;
};

const App = () => {
  return (
    <HashRouter>
      <div>
        <Routes>
          <Route path="/" element={<SlideshowWrapper />} />
        </Routes>
      </div>
    </HashRouter>
  );
};

export default App;
