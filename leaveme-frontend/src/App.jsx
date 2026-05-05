import { useState } from "react";
import { login } from "./services/auth";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    setLoading(true);
    setResult(null);

    try {
      const res = await login(username, password);
      setResult({
        success: true,
        data: res
      });
    } catch (err) {
      console.log(err);
    
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

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1>LeaveMe Login</h1>

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

