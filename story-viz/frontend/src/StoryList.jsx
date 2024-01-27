import React, { useState, useEffect } from 'react';
import { fetchAllStories, publishStory } from './api';
import { useToken } from './TokenContext'
import { useNavigate } from 'react-router-dom'; // or useNavigate in React Router v6
import { useError } from './ErrorContext';
import ErrorMessage from './ErrorMessage';

const StoryList = () => {
  const [stories, setStories] = useState([]);
  const { token } = useToken();
  const navigate = useNavigate();
  const { setError } = useError();

  useEffect(() => {
    // Fetch the list of stories
    fetchAllStories(token)
      .then(allStories => setStories(allStories))
      .catch(error => {
        console.error('Error fetching stories:', error);
      });
  }, []);

  const handlePublish = async (storyId) => {
  
    try {
      await publishStory(storyId, token);
      navigate("/");
    } catch (error) {
      setError('Error posting selections:', error);
    }
  };  

  const isValidStory = story => {
    return story 
      && story.pages
      && story.pages.length > 0
      && story.pages[0].image_urls
      && story.pages[0].paragraph;
  };

  const getStoryImageUrl = story => {
    if ( story.pages[0].image_urls.length > 0 ) {
        return story.pages[0].image_urls[0];
      }

      return null;
  };

  return (
    <div>
      <ErrorMessage />
      <table>
        <tbody>
          {stories && stories.filter(isValidStory).map(story => (
            <tr key={story._id.$oid}>
              <td><button onClick={() => navigate(`/story/${story._id.$oid}`)}>Edit</button></td>
              <td><button onClick={() => handlePublish(story._id.$oid)}>Publish</button></td>
              <td><img src={getStoryImageUrl(story)} width="100" height="100" onClick={() => navigate(`/story/${story._id.$oid}`)}></img></td>
              <td>{story.pages[0].paragraph}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StoryList;