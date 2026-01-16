function MainLayout({ children }) {
  return (
    <div style={{ minHeight: "100vh", background: "#f5f7fb" }}>
      <header
        style={{
          padding: "16px 24px",
          background: "#1e293b",
          color: "white",
          fontSize: "20px",
          fontWeight: "600",
        }}
      >
        Distributed Rate Limiter – Admin Dashboard
      </header>

      <main style={{ padding: "24px" }}>{children}</main>
    </div>
  );
}

export default MainLayout;
