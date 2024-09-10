import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const loginWithCanvasToken = async (canvasToken) => {
  try {
    const response = await axios.post(`${API_URL}/auth/token`, { canvas_token: canvasToken });
    return response.data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

export const getUserInfo = async () => {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('No token found');
  }
  try {
    const response = await axios.get(`${API_URL}/user`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    console.error('Error getting user info:', error);
    throw error;
  }
};

export const getCourses = async () => {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('No token found');
  }
  try {
    const response = await axios.get(`${API_URL}/courses`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    console.error('Error getting courses:', error);
    throw error;
  }
};