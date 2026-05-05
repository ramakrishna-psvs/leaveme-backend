import LeaveForm from "../components/leaveform";

export default function Dashboard() {
  const role = localStorage.getItem("role");

  return (
    <div>
      <h1>Dashboard</h1>

      {role === "employee" && (
        <>
          <LeaveForm />
        </>
      )}

      {role === "employer" && (
        <h2>Employer Dashboard (coming next)</h2>
      )}
    </div>
  );
}
