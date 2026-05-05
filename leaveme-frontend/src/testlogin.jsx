import { useState } from "react";
import { login } from "./services/auth";

export default function TestLogin() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [result, setResult] = useState("");

  const handleLogin = async () => {
    try {
      const res = await login(username, password);
      setResult(JSON.stringify(res, null, 2));
    } catch (err) {
      setResult(err.response?.data?.detail || "Error logging in");
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Test Login</h2>

      <input
        placeholder="username"
        onChange={(e) => setUsername(e.target.value)}
      />

      <br />

      <input
        placeholder="password"
        type="password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <br />

      <button onClick={handleLogin}>Login</button>

      <pre>{result}</pre>
    </div>
  );
}

