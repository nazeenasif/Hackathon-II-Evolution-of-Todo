import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Create base axios instance
const baseApiClient = axios.create({
  baseURL: API_BASE_URL,
});

// Function to create API client with auth token (to be used in client components)
export const createApiClient = (token = null) => {
  const apiClient = axios.create({
    baseURL: API_BASE_URL,
  });

  // Add JWT token to all requests if available
  if (token) {
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  // Handle token expiration and other errors
  apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        // Remove token and redirect to login (handled by calling component)
        if (typeof window !== 'undefined') {
          localStorage.removeItem('jwt_token');
        }
      } else if (error.response?.status >= 500) {
        // Server error - log for monitoring
        console.error('Server error:', error.response);
      }
      return Promise.reject(error);
    }
  );

  return apiClient;
};

// Default export for server-side usage (without auth)
export default baseApiClient;