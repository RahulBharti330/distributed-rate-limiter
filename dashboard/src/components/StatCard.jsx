function StatCard({ title, value, color }) {
  return (
    <div
      style={{
        background: "white",
        padding: "20px",
        borderRadius: "10px",
        flex: 1,
        boxShadow: "0 4px 10px rgba(0,0,0,0.05)",
        borderLeft: `5px solid ${color}`,
      }}
    >
      <p style={{ color: "#64748b", marginBottom: "8px" }}>{title}</p>
      <h2 style={{ margin: 0 }}>{value}</h2>
    </div>
  );
}

export default StatCard;
