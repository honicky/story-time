import axios from 'axios';

const authorizationHeader = import.meta.env.VITE_AUTHORIZATION;
const headers = {"Authorization": `Basic ${authorizationHeader}`};
const referrerPolicy = "origin";
const requestParams = { headers, referrerPolicy };
// const requestParams = { header };

const baseApiUrls = {
  dev: "https://81rq7.apps.beam.cloud",
  staging: "https://ri8tb.apps.beam.cloud",
  production: "https://2oihh.apps.beam.cloud",
};
const baseApiUrl = baseApiUrls[import.meta.env.VITE_STAGE || "dev"] ;

const fetchAllStories = async (storyId) => {
  const storyUrl = `${baseApiUrl}/story/`;
  const response = await axios.get(storyUrl, requestParams);
  return response.data;
};

const fetchStoryData = async (storyId) => {
  const storyUrl = `${baseApiUrl}/story/${storyId}`;
  const response = await axios.get(storyUrl, requestParams);
  return response.data;
};

const fetchSelectionsData = async (storyId) => {
  try {
      const selectionsUrl = `${baseApiUrl}/story/${storyId}/selections`;
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
  await axios.post(`${baseApiUrl}/story/${storyId}/selections`, payload);
}
export { fetchAllStories, fetchStoryData, fetchSelectionsData, postSelections };
