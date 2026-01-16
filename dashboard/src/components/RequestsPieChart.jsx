import { PieChart, Pie, Tooltip, ResponsiveContainer } from "recharts";

function RequestsPieChart({ data }) {
  return (
    <div style={{ height: 300, background: "white", padding: 20, borderRadius: 10 }}>
      <h3>Traffic Distribution</h3>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie data={data} dataKey="count" nameKey="name" />
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default RequestsPieChart;
