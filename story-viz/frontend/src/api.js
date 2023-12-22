import axios from 'axios';

const authorizationHeader = import.meta.env.VITE_AUTHORIZATION;
const headers = {"Authorization": `Basic ${authorizationHeader}`};
const referrerPolicy = "origin";
const requestParams = { headers, referrerPolicy }

const fetchStoryData = async (storyId) => {
  const storyUrl = `https://81rq7.apps.beam.cloud/story/${storyId}`;
  const response = await axios.get(storyUrl, requestParams);
  return response.data;
};

const fetchSelectionsData = async (storyId) => {
  try {
      const selectionsUrl = `https://81rq7.apps.beam.cloud/story/${storyId}/selections`;
      const response = await axios.get(selectionsUrl, requestParams);
      return response.data;
  } catch (error) {
    if (error.response && error.response.status === 404) {
      return []; // Set selections to an empty array if 404
    } else {
      throw error;
    }
  }
};

const postSelections = async (storyId, selectedImages) => {
  const payload = {
    page_selections: selectedImages
  };
  await axios.post(`https://81rq7.apps.beam.cloud/story/${storyId}/selections`, payload);
}
export { fetchStoryData, fetchSelectionsData, postSelections };
