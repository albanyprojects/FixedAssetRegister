
import { useEffect, useState } from "react";

function Employee() {
  const [employees, setEmployees] = useState<any[]>([]);
  const [departments, setDepartments] = useState<any[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [editingEmployee, setEditingEmployee] = useState<any>(null);

  const [formData, setFormData] = useState({
    EmployeeID: "",
    FirstName: "",
    LastName: "",
    Email: "",
    DepartmentID: "",
  });

  useEffect(() => {
    fetch("http://127.0.0.1:8000/employees")
      .then((response) => response.json())
      .then((data) => {
        console.log("EMPLOYEES RECEIVED:", data);
        setEmployees(data);
      })
      .catch((error) => {
        console.error("Error fetching employees:", error);
      });

    fetch("http://127.0.0.1:8000/departments")
      .then((response) => response.json())
      .then((data) => {
        console.log("DEPARTMENTS RECEIVED:", data);
        setDepartments(data);
      })
      .catch((error) => {
        console.error("Error fetching departments:", error);
      });
  }, []);

  function refreshEmployees() {
    fetch("http://127.0.0.1:8000/employees")
      .then((response) => response.json())
      .then((data) => {
        setEmployees(data);
      })
      .catch((error) => {
        console.error("Error refreshing employees:", error);
      });
  }

  function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  }

  function handleSelectChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ) {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  }

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    const url = editingEmployee
      ? `http://127.0.0.1:8000/employees/${editingEmployee.EmployeeID}`
      : "http://127.0.0.1:8000/employees";

    const method = editingEmployee ? "PUT" : "POST";

    fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Employee Saved:", data);

        setShowForm(false);
        setEditingEmployee(null);
        refreshEmployees();
      })
      .catch((error) => {
        console.error("There was an error saving an employee:", error);
      });
  }

  function handleDelete(employeeID: number) {
    fetch(`http://127.0.0.1:8000/employees/${employeeID}`, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Employee deleted:", data);
        refreshEmployees();
      })
      .catch((error) => {
        console.error("There was an error deleting this employee:", error);
      });
  }

  return (
    <div>
      <h1>Employees</h1>

      <p style={{ color: "red", fontSize: "20px" }}>
        Employee count: {employees.length}
      </p>

      <button onClick={() => setShowForm(true)}>
        Add Employee
      </button>

      <button onClick={refreshEmployees}>
        Refresh
      </button>

      {showForm && (
        <div>
          <h2>Add Employee</h2>

          <div>
            <label>First Name</label>
            <br />
            <input
              type="text"
              name="FirstName"
              value={formData.FirstName}
              onChange={handleChange}
            />
          </div>

          <div>
            <label>Last Name</label>
            <br />
            <input
              type="text"
              name="LastName"
              value={formData.LastName}
              onChange={handleChange}
            />
          </div>

          <div>
            <label>Email</label>
            <br />
            <input
              type="email"
              name="Email"
              value={formData.Email}
              onChange={handleChange}
            />
          </div>

          <div>
            <label>Department</label>
            <br />
            <select
              name="DepartmentID"
              value={formData.DepartmentID}
              onChange={handleSelectChange}
            >
              <option value="">-- Select Department --</option>

              {departments.map((department: any) => (
                <option
                  key={department.DepartmentID}
                  value={department.DepartmentID}
                >
                  ID {department.DepartmentID} - ({department.DepartmentName})
                </option>
              ))}
            </select>
          </div>

          <br />

          <button onClick={handleSubmit}>
            Save
          </button>
        </div>
      )}

      {employees.length === 0 ? (
        <p>No employees found.</p>
      ) : (
        <table style={{ border: "2px solid red" }}>
          <thead>
            <tr style={{ border: "1px solid blue" }}>
              <th>EmployeeID</th>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Email</th>
              <th>Department ID</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {employees.map((employee: any) => (
              <tr
                key={employee.EmployeeID}
                style={{ border: "1px solid blue" }}
              >
                <td>{employee.EmployeeID}</td>
                <td>{employee.FirstName}</td>
                <td>{employee.LastName}</td>
                <td>{employee.Email}</td>
                <td>{employee.DepartmentID}</td>

                <td>
                  <button
                    onClick={() => {
                      setEditingEmployee(employee);
                      setFormData(employee);
                      setShowForm(true);
                    }}
                  >
                    Edit
                  </button>

                  <button
                    onClick={() =>
                      handleDelete(employee.EmployeeID)
                    }
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default Employee;

