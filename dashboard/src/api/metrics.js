import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

export const fetchMetrics = async () => {
  const response = await axios.get(`${API_BASE_URL}/admin/metrics`);
  return response.data;
};
