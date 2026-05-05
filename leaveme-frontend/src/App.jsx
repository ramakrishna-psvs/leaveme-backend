import { useState } from "react";
import { login } from "./services/auth";
import axios from "axios";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Leave form state
  const [reason, setReason] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const handleLogin = async () => {
    setLoading(true);
    setResult(null);

    try {
      const res = await login(username, password);

      setToken(res.access_token); // 🔥 store JWT

      setResult({
        success: true,
        message: "Login successful"
      });
    } catch (err) {
      setResult({
        success: false,
        error:
          err.response?.data?.detail ||
          err.message ||
          "Login failed"
      });
    }

    setLoading(false);
  };

  const handleLeaveSubmit = async () => {
    try {
      const res = await axios.post(
        "https://leaveme-backend-production.up.railway.app/leave/request",
        {
          reason,
          start_date: startDate,
          end_date: endDate
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setResult({
        success: true,
        message: "Leave submitted!",
        data: res.data
      });
    } catch (err) {
      setResult({
        success: false,
        error: err.response?.data?.detail || "Leave failed"
      });
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1>LeaveMe</h1>

        {/* 🔹 If NOT logged in → show login */}
        {!token ? (
          <>
            <input
              style={styles.input}
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />

            <input
              style={styles.input}
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <button
              style={styles.button}
              onClick={handleLogin}
              disabled={loading}
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </>
        ) : (
          /* 🔹 If logged in → show leave form */
          <>
            <h3>Request Leave</h3>

            <input
              style={styles.input}
              placeholder="Reason"
              value={reason}
              onChange={(e) => setReason(e.target.value)}
            />

            <input
              style={styles.input}
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
            />

            <input
              style={styles.input}
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
            />

            <button style={styles.button} onClick={handleLeaveSubmit}>
              Submit Leave
            </button>
          </>
        )}

        {result && (
          <pre style={styles.result}>
            {JSON.stringify(result, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#0f172a",
    color: "white",
    fontFamily: "Arial"
  },
  card: {
    padding: 30,
    background: "#1e293b",
    borderRadius: 12,
    width: 300,
    display: "flex",
    flexDirection: "column",
    gap: 10
  },
  input: {
    padding: 10,
    borderRadius: 6,
    border: "none"
  },
  button: {
    padding: 10,
    background: "#3b82f6",
    color: "white",
    border: "none",
    borderRadius: 6,
    cursor: "pointer"
  },
  result: {
    marginTop: 10,
    fontSize: 12,
    background: "#0f172a",
    padding: 10,
    borderRadius: 6
  }
};

export default App;
