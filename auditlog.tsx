import { useEffect, useState } from "react";      // this only actually uses the one crud, reason being is that users should not be able to create, delete or modify an audit log, it should be read only and only modifiable by modifying other tables, which itself, gets audited.

function AuditLog() {
  const [auditLogs, setAuditLogs] = useState<any[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/auditlogs")
      .then((response) => response.json())
      .then((data) => {
        console.log("AUDIT LOGS RECEIVED:", data);  //this doesnt show in the uvicorn terminal, instead it shows in powershell if you have it opened on this folder. it also doesnt show on the react frontend. but you can see it if you insepct the frontend as a debugging tool
        setAuditLogs(data);
      })
      .catch((error) => {
        console.error("Error fetching audit logs:", error);
      });
  }, []);

  function refreshAuditLogs() {
    fetch("http://127.0.0.1:8000/auditlogs")  // the backend auditlog swagger UI, dont actually use on swagger though, it will crash your computer if theres too much backlogged data
      .then((response) => response.json())
      .then((data) => {
        setAuditLogs(data);
      })
      .catch((error) => { 
        console.error("Error refreshing audit logs:", error); //this error actually plays even when the refreshes are correct. but it is only visible outside of inspect element when no data shows
      });
  }
//--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  return (
    <div>
      <h1>Audit Log</h1>

      <p style={{ color: "red", fontSize: "20px" }}>
        Audit entries: {auditLogs.length}
      </p>

      <button onClick={refreshAuditLogs}>
        Refresh
      </button>

      {auditLogs.length === 0 ? (
        <p>No audit records found.</p>
      ) : (
        <table style={{ border: "2px solid red" }}>
          <thead>
            <tr style={{ border: "1px solid blue" }}>
              <th>Audit ID</th>
              <th>Table</th>
              <th>Record ID</th>
              <th>Field</th>
              <th>Old Value</th>
              <th>New Value</th>
              <th>Action</th>
              <th>Changed By</th>
            </tr>
          </thead>

          <tbody>
            {auditLogs.map((log: any) => (
              <tr
                key={log.AuditID}
                style={{ border: "1px solid blue" }}
              >
                <td>{log.AuditID}</td>
                <td>{log.TableName}</td>
                <td>{log.RecordID}</td> 
                <td>{log.FieldName}</td>
                <td>{log.OldValue}</td>
                <td>{log.NewValue}</td>
                <td>{log.Action}</td>
                <td>{log.ChangedBy}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default AuditLog;
