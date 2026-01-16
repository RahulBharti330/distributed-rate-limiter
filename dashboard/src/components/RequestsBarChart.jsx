import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function RequestsBarChart({ data }) {
  return (
    <div style={{ height: 300, background: "white", padding: 20, borderRadius: 10 }}>
      <h3>Allowed vs Blocked Requests</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default RequestsBarChart;
