import { useQuery } from "@tanstack/react-query";
import { fetchMetrics } from "../api/metrics";

export const useMetrics = () => {
  return useQuery({
    queryKey: ["metrics"],
    queryFn: fetchMetrics,
    refetchInterval: 5000, // refresh every 5 seconds
  });
};
