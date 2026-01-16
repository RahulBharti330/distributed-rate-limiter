import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/" element={<h1>Rate Limiter Dashboard</h1>} />
    </Routes>
  );
}

export default App;
