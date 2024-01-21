import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { fetchAllStories } from './api';

const StoryList = () => {
 const [stories, setStories] = useState([]);

 useEffect(() => {
   // Fetch the list of stories
  fetchAllStories()
    .then(response => setStories(response.data))
    .catch(error => {
      console.error('Error fetching stories:', error);
    });
 }, []);

 return (
   <div>
     <table>
       <tbody>
         {stories && stories.map(story => (
           <tr key={story._id.$oid}>
             <td><button>Edit</button></td>
             <td><button>Publish</button></td>
             <td><img url={story.pages[0].image_urls[0]} width="20" height="20"></img></td>
             <td>{story.pages[0].paragraph}</td>
           </tr>
         ))}
       </tbody>
     </table>
   </div>
 );
};

export default StoryList;