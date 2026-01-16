import MainLayout from "../layouts/MainLayout";
import StatCard from "../components/StatCard";
import RequestsBarChart from "../components/RequestsBarChart";
import RequestsPieChart from "../components/RequestsPieChart";
import { useMetrics } from "../hooks/useMetrics";
import SimulationControl from "../components/SimulationControl";


function Overview() {
  const { data, isLoading, isError } = useMetrics();

  if (isLoading) return <p>Loading metrics...</p>;
  if (isError) return <p>Failed to load metrics</p>;

  const chartData = [
    { name: "Allowed", count: data.allowed_requests },
    { name: "Blocked", count: data.blocked_requests },
  ];

  return (
    <MainLayout>
        <SimulationControl />
      <div style={{ display: "flex", gap: "20px", marginBottom: "24px" }}>
        <StatCard
          title="Total Requests"
          value={data.total_requests}
          color="#0ea5e9"
        />
        <StatCard
          title="Allowed Requests"
          value={data.allowed_requests}
          color="#22c55e"
        />
        <StatCard
          title="Blocked Requests"
          value={data.blocked_requests}
          color="#ef4444"
        />
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px" }}>
        <RequestsBarChart data={chartData} />
        <RequestsPieChart data={chartData} />
      </div>
    </MainLayout>
  );
}

export default Overview;
