
import { useEffect, useState } from "react";

function Device() {
  const [devices, setDevices] = useState<any[]>([]);
  const [deviceTypes, setDeviceTypes] = useState<any[]>([]);
  const [departments, setDepartments] = useState<any[]>([]);
  const [employees, setEmployees] = useState<any[]>([]);

  const [showForm, setShowForm] = useState(false);
  const [editingDevice, setEditingDevice] = useState<any>(null);

  const [formData, setFormData] = useState({
    AssetTag: "",
    DeviceTypeID: "",
    Manufacturer: "",
    Model: "",
    SerialNumber: "",
    PurchaseDate: "",
    PurchaseCost: "",
    DepartmentID: "",
    EmployeeID: "",
  });

  useEffect(() => {
    fetch("http://127.0.0.1:8000/devices")
      .then((response) => response.json())
      .then((data) => {
        console.log("DEVICES RECEIVED:", data);
        setDevices(data);
      })
      .catch((error) => {
        console.error("Error fetching devices:", error);
      });

    fetch("http://127.0.0.1:8000/devicetypes")
      .then((response) => response.json())
      .then((data) => {
        console.log("DEVICE TYPES RECEIVED:", data);
        setDeviceTypes(data);
      })
      .catch((error) => {
        console.error("Error fetching device types:", error);
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

    fetch("http://127.0.0.1:8000/employees")
      .then((response) => response.json())
      .then((data) => {
        console.log("EMPLOYEES RECEIVED:", data);
        setEmployees(data);
      })
      .catch((error) => {
        console.error("Error fetching employees:", error);
      });
  }, []);

  function refreshDevices() {
    fetch("http://127.0.0.1:8000/devices")
      .then((response) => response.json())
      .then((data) => {
        setDevices(data);
      })
      .catch((error) => {
        console.error("Error refreshing devices:", error);
      });
  }

  function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  }

  function handleSelectChange(event: React.ChangeEvent<HTMLSelectElement>) {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  }

  function handleDateChange(event: React.ChangeEvent<HTMLInputElement>) {
    let value = event.target.value.replace(/\D/g, "");

    if (value.length > 8) {
      value = value.substring(0, 8);
    }

    let formatted = value;

    if (value.length >= 5) {
      formatted =
        value.substring(0, 2) +
        "/" +
        value.substring(2, 4) +
        "/" +
        value.substring(4);
    } else if (value.length >= 3) {
      formatted =
        value.substring(0, 2) +
        "/" +
        value.substring(2);
    }

    setFormData({
      ...formData,
      PurchaseDate: formatted,
    });
  }

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    const url = editingDevice
      ? `http://127.0.0.1:8000/devices/${editingDevice.DeviceID}`
      : "http://127.0.0.1:8000/devices";

    const method = editingDevice ? "PUT" : "POST";

    const submissionData = {
      ...formData,
      PurchaseDate: formData.PurchaseDate
        .split("/")
        .reverse()
        .join("-"),
    };

    fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(submissionData),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Device Saved:", data);

        setShowForm(false);
        setEditingDevice(null);
        refreshDevices();
      })
      .catch((error) => {
        console.error("There was an error saving a device:", error);
      });
  }

  function handleDelete(deviceID: number) {
    fetch(`http://127.0.0.1:8000/devices/${deviceID}`, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Device deleted:", data);
        refreshDevices();
      })
      .catch((error) => {
        console.error("There was an error deleting this device:", error);
      });
  }

  return (
    <div>
      <h1>Devices</h1>

      <p style={{ color: "red", fontSize: "20px" }}>
        Device count: {devices.length}
      </p>

      <button onClick={() => setShowForm(true)}>
        Add Device
      </button>

      <button onClick={refreshDevices}>
        Refresh
      </button>

      {showForm && (
        <div>
          <h2>Add Device</h2>

          <div>
            <label>Asset Tag</label>
            <br />
            <input
              type="text"
              name="AssetTag"
              value={formData.AssetTag}
              onChange={handleChange}
            />
          </div>

          <div>
            <label>Device Type</label>
            <br />
            <select
              name="DeviceTypeID"
              value={formData.DeviceTypeID}
              onChange={handleSelectChange}
            >
              <option value="">-- Select Device Type --</option>

              {deviceTypes.map((deviceType: any) => (
                <option
                  key={deviceType.DeviceTypeID}
                  value={deviceType.DeviceTypeID}
                >
                  ID {deviceType.DeviceTypeID} - ({deviceType.DeviceTypeName})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label>Manufacturer</label>
            <br />
            <input
              type="text"
              name="Manufacturer"
              value={formData.Manufacturer}
              onChange={handleChange}
            />
          </div>

          <div>
            <label>Model</label>
            <br />
            <input
              type="text"
              name="Model"
              value={formData.Model}
              onChange={handleChange}
            />
          </div>

          <div>
            <label>Serial Number</label>
            <br />
            <input
              type="text"
              name="SerialNumber"
              value={formData.SerialNumber}
              onChange={handleChange}
            />
          </div>

          <div>
            <label>Purchase Date</label>
            <br />
            <input
              type="text"
              name="purchaseDate"
              value={formData.PurchaseDate}
              onChange={handleDateChange}
              placeholder="DD/MM/YYYY"
            />
          </div>

          <div>
            <label>Purchase Cost</label>
            <br />
            <input
              type="number"
              name="PurchaseCost"
              value={formData.PurchaseCost}
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

          <div>
            <label>Employee</label>
            <br />
            <select
              name="EmployeeID"
              value={formData.EmployeeID}
              onChange={handleSelectChange}
            >
              <option value="">-- Select Employee --</option>

              {employees.map((employee: any) => (
                <option
                  key={employee.EmployeeID}
                  value={employee.EmployeeID}
                >
                  ID {employee.EmployeeID} - ({employee.FirstName} - {employee.LastName})
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

      {devices.length === 0 ? (
        <p>No devices found.</p>
      ) : (
        <table style={{ border: "2px solid red" }}>
          <thead>
            <tr style={{ border: "1px solid blue" }}>
              <th>DeviceID</th>
              <th>Asset Tag</th>
              <th>Device Type</th>
              <th>Manufacturer</th>
              <th>Model</th>
              <th>Serial Number</th>
              <th>Purchase Cost</th>
              <th>Actions</th>
              <th>PurchaseDate</th>
            </tr>
          </thead>

          <tbody>
            {devices.map((device: any) => (
              <tr
                key={device.DeviceID}
                style={{ border: "1px solid blue" }}
              >
                <td>{device.DeviceID}</td>
                <td>{device.AssetTag}</td>
                <td>{device.DeviceType}</td>
                <td>{device.Manufacturer}</td>
                <td>{device.Model}</td>
                <td>{device.SerialNumber}</td>
                <td>{device.PurchaseCost}</td>
                <td>{device.DeviceType}</td>
                <td>{device.PurchaseDate}</td>

                <td>
                  <button
                    onClick={() => {
                      setEditingDevice(device);
                      setFormData(device);
                      setShowForm(true);
                    }}
                  >
                    Edit
                  </button>

                  <button
                    onClick={() => handleDelete(device.DeviceID)}
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

export default Device;

