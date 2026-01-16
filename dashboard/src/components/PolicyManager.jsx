import { useState } from "react";
import axios from "axios";

function PolicyManager() {
  const [tier, setTier] = useState("free");
  const [capacity, setCapacity] = useState("");
  const [refillRate, setRefillRate] = useState("");

  const updatePolicy = async () => {
    await axios.post("http://localhost:8000/admin/policy/update", {
      tier,
      capacity: Number(capacity),
      refill_rate: Number(refillRate),
    });

    alert(`Policy updated for ${tier} tier`);
  };

  return (
    <div className="policy-card">
      <h3>Rate Limit Policy Manager</h3>

      <div className="policy-grid">
        <div className="field">
          <label>User Tier</label>
          <select value={tier} onChange={(e) => setTier(e.target.value)}>
            <option value="free">Free</option>
            <option value="premium">Premium</option>
            <option value="enterprise">Enterprise</option>
          </select>
        </div>

        <div className="field">
          <label>Token Bucket Capacity</label>
          <input
            type="number"
            placeholder="e.g. 100"
            value={capacity}
            onChange={(e) => setCapacity(e.target.value)}
          />
        </div>

        <div className="field">
          <label>Refill Rate (tokens/sec)</label>
          <input
            type="number"
            placeholder="e.g. 50"
            value={refillRate}
            onChange={(e) => setRefillRate(e.target.value)}
          />
        </div>
      </div>

      <button className="primary" onClick={updatePolicy}>
        Update Policy
      </button>
    </div>
  );
}

export default PolicyManager;
