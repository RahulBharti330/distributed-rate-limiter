import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const fetchMetrics = async () => {
  const response = await axios.get(`${API_BASE_URL}/admin/metrics`);
  return response.data;
};
