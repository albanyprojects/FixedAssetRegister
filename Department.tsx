import { useEffect, useState } from "react";

function Department() {
  const [departments, setDepartments] = useState<any[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [editingDepartment, setEditingDepartment] = useState<any>(null);

  const [formData, setFormData] = useState({
    DepartmentName: "",
  });
                                                                                     ///creates dynamic table
  useEffect(() => {                                                                                     ///creates dynamic table
    fetch("http://127.0.0.1:8000/departments")                                                                                     ///creates dynamic table
      .then((response) => response.json())                                                                                     ///creates dynamic table
      .then((data) => {                                                                                     ///creates dynamic table
        console.log("DEPARTMENTS RECEIVED:", data);                                                                                     ///creates dynamic table
        setDepartments(data);                                                                                     ///creates dynamic table
      })                                                                                     ///creates dynamic table
      .catch((error) => {                                                                                     ///creates dynamic table
        console.error("Error fetching departments:", error);                                                                                     ///creates dynamic table
      });
  }, []);
//------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  function refreshDepartments() {
    fetch("http://127.0.0.1:8000/departments")
      .then((response) => response.json())
      .then((data) => {
        setDepartments(data);
      })
      .catch((error) => {
        console.error("Error refreshing departments:", error);
      });
  }
//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  }
//------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    const url = editingDepartment
      ? `http://127.0.0.1:8000/departments/${editingDepartment.DepartmentID}`
      : "http://127.0.0.1:8000/departments"; 

    const method = editingDepartment ? "PUT" : "POST";

    fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Department Saved:", data);

        setShowForm(false);
        setEditingDepartment(null);
        refreshDepartments();
      })
      .catch((error) => {
        console.error("There was an error saving the department:", error);
      });
  }
//------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  function handleDelete(departmentID: number) {
    fetch(`http://127.0.0.1:8000/departments/${departmentID}`, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Department deleted:", data);
        refreshDepartments();
      })
      .catch((error) => {
        console.error("There was an error deleting this department:", error);
      });
  }

  return (
    <div>
      <h1>Departments</h1>

      <p style={{ color: "red", fontSize: "20px" }}>
        Department count: {departments.length}
      </p>

      <button onClick={() => setShowForm(true)}>
        Add Department
      </button>

      <button onClick={refreshDepartments}>
        Refresh
      </button>

      {showForm && (
        <div>
          <h2>Add Department</h2>

          <div>
            <label>Department Name</label>
            <br />
            <input
              type="text"
              name="DepartmentName"
              value={formData.DepartmentName}
              onChange={handleChange}
            />
          </div>

          <br />

          <button onClick={handleSubmit}>
            Save
          </button>
        </div>
      )}

      {departments.length === 0 ? (
        <p>No departments found.</p>
      ) : (
        <table style={{ border: "2px solid red" }}>
          <thead>
            <tr style={{ border: "1px solid blue" }}>
              <th>Department ID</th>
              <th>Department Name</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {departments.map((department: any) => (
              <tr
                key={department.DepartmentID}
                style={{ border: "1px solid blue" }}
              >
                <td>{department.DepartmentID}</td>
                <td>{department.DepartmentName}</td>

                <td>
                  <button
                    onClick={() => {
                      setEditingDepartment(department);
                      setFormData(department);
                      setShowForm(true);
                    }}
                  >
                    Edit
                  </button>

                  <button
                    onClick={() => handleDelete(department.DepartmentID)}
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

export default Department;
