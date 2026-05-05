import { useState } from "react";

export default function LeaveForm() {
  const [reason, setReason] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const submitLeave = async () => {
    const token = localStorage.getItem("token");

    const res = await fetch(
      "https://leaveme-backend-production.up.railway.app/leaves/create",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          reason,
          start_date: startDate,
          end_date: endDate,
        }),
      }
    );

    const data = await res.json();
    console.log(data);
  };

  return (
    <div>
      <h2>Request Leave</h2>

      <input
        placeholder="Reason"
        onChange={(e) => setReason(e.target.value)}
      />

      <input
        type="date"
        onChange={(e) => setStartDate(e.target.value)}
      />

      <input
        type="date"
        onChange={(e) => setEndDate(e.target.value)}
      />

      <button onClick={submitLeave}>Submit</button>
    </div>
  );
}
