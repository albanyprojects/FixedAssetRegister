import { useEffect, useState } from "react";

function DeviceType() {
  const [deviceTypes, setDeviceTypes] = useState<any[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [editingDeviceType, setEditingDeviceType] = useState<any>(null);

  const [formData, setFormData] = useState({
    DeviceTypeName: "",
  });

  useEffect(() => {
    fetch("http://127.0.0.1:8000/devicetypes")
      .then((response) => response.json())
      .then((data) => {
        console.log("DEVICE TYPES RECEIVED:", data);
        setDeviceTypes(data);
      })
      .catch((error) => {
        console.error("Error fetching device types:", error);
      });
  }, []);

  function refreshDeviceTypes() {
    fetch("http://127.0.0.1:8000/devicetypes")
      .then((response) => response.json())
      .then((data) => {
        setDeviceTypes(data);
      })
      .catch((error) => {
        console.error("Error refreshing device types:", error);
      });
  }

  function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  }

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    const url = editingDeviceType
      ? `http://127.0.0.1:8000/device-types/${editingDeviceType.DeviceTypeID}`
      : "http://127.0.0.1:8000/device-types";

    const method = editingDeviceType ? "PUT" : "POST";

    fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Device Type Saved:", data);

        setShowForm(false);
        setEditingDeviceType(null);
        refreshDeviceTypes();
      })
      .catch((error) => {
        console.error("There was an error saving the device type:", error);
      });
  }

  function handleDelete(deviceTypeID: number) {
    fetch(`http://127.0.0.1:8000/device-types/${deviceTypeID}`, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Device Type deleted:", data);
        refreshDeviceTypes();
      })
      .catch((error) => {
        console.error("There was an error deleting this device type:", error);
      });
  }

  return (
    <div>
      <h1>Device Types</h1>

      <p style={{ color: "red", fontSize: "20px" }}>
        Device Type count: {deviceTypes.length}
      </p>

      <button onClick={() => setShowForm(true)}>
        Add Device Type
      </button>

      <button onClick={refreshDeviceTypes}>
        Refresh
      </button>

      {showForm && (
        <div>
          <h2>Add Device Type</h2>

          <div>
            <label>Device Type Name</label>
            <br />
            <input
              type="text"
              name="DeviceTypeName"
              value={formData.DeviceTypeName}
              onChange={handleChange}
            />
          </div>

          <br />

          <button onClick={handleSubmit}>
            Save
          </button>
        </div>
      )}

      {deviceTypes.length === 0 ? (
        <p>No device types found.</p>
      ) : (
        <table style={{ border: "2px solid red" }}>
          <thead>
            <tr style={{ border: "1px solid blue" }}>
              <th>Device Type ID</th>
              <th>Device Type Name</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {deviceTypes.map((deviceType: any) => (
              <tr
                key={deviceType.DeviceTypeID}
                style={{ border: "1px solid blue" }}
              >
                <td>{deviceType.DeviceTypeID}</td>
                <td>{deviceType.DeviceTypeName}</td>

                <td>
                  <button
                    onClick={() => {
                      setEditingDeviceType(deviceType);
                      setFormData(deviceType);
                      setShowForm(true);
                    }}
                  >
                    Edit
                  </button>

                  <button
                    onClick={() => handleDelete(deviceType.DeviceTypeID)}
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

export default DeviceType;
