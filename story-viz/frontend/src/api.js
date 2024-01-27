import axios from 'axios';

const defaultHeaders = {};
const baseApiUrl = "/api"

const getHeadersWithAuthorization = (token) => {
  const headers = structuredClone(defaultHeaders);
  headers["Authorization"] = `Bearer ${token}`
  return headers
}

const fetchAllStories = async (token) => {
  const headers = getHeadersWithAuthorization(token);

  const storyUrl = `${baseApiUrl}/story/`;
  const response = await axios.get(storyUrl, {headers});
  return response.data;
};

const fetchStoryData = async (storyId, token) => {
  const headers = getHeadersWithAuthorization(token);
  
  const storyUrl = `${baseApiUrl}/story/${storyId}`;
  const response = await axios.get(storyUrl, {headers});
  return response.data;
};

const fetchSelectionsData = async (storyId, token) => {
  try {
    const headers = getHeadersWithAuthorization(token);

    const selectionsUrl = `${baseApiUrl}/story/${storyId}/selections`;
      const response = await axios.get(selectionsUrl, {headers});
      return response.data;
  } catch (error) {
    if (error?.response?.status === 404) {
      return []; // Set selections to an empty array if 404
    } else {
      throw error;
    }
  }
};

const postSelections = async (storyId, selectedImages, token) => {
  const headers = getHeadersWithAuthorization(token);
  const payload = {
    page_selections: selectedImages
  };
  await axios.post(`${baseApiUrl}/story/${storyId}/selections`, payload, {headers});
}

const publishStory = async (storyId, token) => {
  const headers = getHeadersWithAuthorization(token);

  await axios.post(`${baseApiUrl}/story/${storyId}/publish`, {}, {headers});
}


const login = async(username, password) => {
  const loginUrl = `${baseApiUrl}/token`

  const params = new URLSearchParams();
  params.append("username", username);
  params.append("password", password);
  const response = await axios.post(loginUrl, params);

  return response.data;

 }

export { fetchAllStories, fetchStoryData, fetchSelectionsData, login, postSelections, publishStory };

