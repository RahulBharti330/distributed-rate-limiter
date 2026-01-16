import axios from "axios";
import { useState } from "react";

function SimulationControl() {
  const [config, setConfig] = useState({
    requests_per_second: "",
    users: "",
    duration_seconds: "",
  });

  const [serverCapacity, setServerCapacity] = useState("");

  const handleChange = (e) => {
    setConfig({ ...config, [e.target.name]: Number(e.target.value) });
  };

  const startSimulation = async () => {
    await axios.post("http://localhost:8000/admin/simulate/start", {
      ...config,
      endpoint: "/api/data",
      user_tier: "free",
    });
  };

  const updateServerCapacity = async () => {
    await axios.post("http://localhost:8000/admin/server-capacity", {
      max_rps: Number(serverCapacity),
    });
  };

  const resetMetrics = async () => {
    await axios.post("http://localhost:8000/admin/metrics/reset");
  };

  return (
    <div className="sim-card">
      <h3>Traffic Simulation</h3>

      <div className="sim-grid">
        <div className="field">
          <label>Requests per second (global)</label>
          <input
            type="number"
            name="requests_per_second"
            placeholder="e.g. 50"
            onChange={handleChange}
          />
        </div>

        <div className="field">
          <label>Concurrent users</label>
          <input
            type="number"
            name="users"
            placeholder="e.g. 5"
            onChange={handleChange}
          />
        </div>

        <div className="field">
          <label>Simulation duration (seconds)</label>
          <input
            type="number"
            name="duration_seconds"
            placeholder="e.g. 60"
            onChange={handleChange}
          />
        </div>

        <div className="field">
          <label>Server capacity (req/sec)</label>
          <input
            type="number"
            placeholder="e.g. 30"
            value={serverCapacity}
            onChange={(e) => setServerCapacity(e.target.value)}
          />
        </div>
      </div>

      <div className="button-row">
        <button className="primary" onClick={updateServerCapacity}>
          Update Server Capacity
        </button>
        <button className="primary" onClick={startSimulation}>
          Start Simulation
        </button>
        <button className="danger" onClick={resetMetrics}>
          Reset Metrics
        </button>
      </div>
    </div>
  );
}

export default SimulationControl;
