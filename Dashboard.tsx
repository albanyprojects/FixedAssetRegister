import { useState } from "react";

const TABLE_FIELDS: Record<string, string[]> = {
  employees: [
    "EmployeeID",
    "FirstName",
    "LastName",
    "Email",
    "DepartmentID",
  ],

  devices: [
    "DeviceID",
    "DeviceTypeID",
    "AssetTag",
    "Model",
    "Manufacturer",
    "SerialNumber",
    "PurchaseDate",
    "PurchaseCost",
    "DepartmentID",
    "EmployeeID",
  ],

  departments: [
    "DepartmentID",
    "DepartmentName",
  ],

  devicetypes: [
    "DeviceTypeID",
    "DeviceTypeName",
  ],

  auditlogs: [
    "AuditID",
    "TableName",
    "RecordID",
    "FieldName",
    "OldValue",
    "NewValue",
    "Action",
    "ChangedBy",
    "ChangeDate",
  ],
};


function Dashboard() {
  const [conditions, setConditions] = useState([
    {
      table: "employees",
      field: "FirstName",
      operator: "contains",
      value: "",
    },
  ]);

  const [results, setResults] = useState<any[]>([]);


  function updateCondition(
    index: number,
    key: string,
    value: string
  ) {
    const updatedConditions = [...conditions];

    updatedConditions[index] = {
      ...updatedConditions[index],
      [key]: value,
    };

    setConditions(updatedConditions);
  }


  function handleTableChange(
    index: number,
    table: string
  ) {
    const updatedConditions = [...conditions];

    updatedConditions[index] = {
      ...updatedConditions[index],
      table: table,
      field: TABLE_FIELDS[table][0],
    };

    setConditions(updatedConditions);
  }


  function addCondition() {
    setConditions([
      ...conditions,
      {
        table: "employees",
        field: "FirstName",
        operator: "contains",
        value: "",
      },
    ]);
  }


  function removeCondition(index: number) {
    if (conditions.length === 1) {
      return;
    }

    const updatedConditions = conditions.filter(
      (_, conditionIndex) => conditionIndex !== index
    );

    setConditions(updatedConditions);
  }


  function handleSearch() {
    fetch("http://127.0.0.1:8000/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        conditions: conditions,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(
            `Search failed with status ${response.status}`
          );
        }

        return response.json();
      })
      .then((data) => {
        setResults(data);
        console.log("SEARCH CONDITIONS:", conditions);
        console.log("SEARCH RESULTS:", data);
      })
      .catch((error) => {
        console.error("Search failed:", error);
      });
  }


  return (
    <div>

      <h1>Dashboard</h1>

      <h3>Search Database</h3>


      {conditions.map((condition, index) => (

        <div key={index}>

          <h4>Condition {index + 1}</h4>


          <label>Table</label>
          <br />

          <select
            value={condition.table}
            onChange={(e) =>
              handleTableChange(
                index,
                e.target.value
              )
            }
          >
            <option value="employees">
              Employee
            </option>

            <option value="devices">
              Device
            </option>

            <option value="departments">
              Department
            </option>

            <option value="devicetypes">
              DeviceType
            </option>

            <option value="auditlogs">
              AuditLog
            </option>
          </select>


          <br />
          <br />


          <label>Field</label>
          <br />

          <select
            value={condition.field}
            onChange={(e) =>
              updateCondition(
                index,
                "field",
                e.target.value
              )
            }
          >

            {TABLE_FIELDS[condition.table].map(
              (field) => (
                <option
                  key={field}
                  value={field}
                >
                  {field}
                </option>
              )
            )}

          </select>


          <br />
          <br />


          <label>Operator</label>
          <br />

          <select
            value={condition.operator}
            onChange={(e) =>
              updateCondition(
                index,
                "operator",
                e.target.value
              )
            }
          >
            <option value="contains">
              Contains
            </option>

            <option value="equals">
              Equals
            </option>

            <option value="greater">
              Greater Than &gt;
            </option>

            <option value="less">
              Less Than &lt;
            </option>
          </select>


          <br />
          <br />


          <label>Search Value</label>
          <br />

          <input
            type="text"
            value={condition.value}
            onChange={(e) =>
              updateCondition(
                index,
                "value",
                e.target.value
              )
            }
            placeholder="Enter search value"
          />


          <br />
          <br />

          {conditions.length > 1 && (
            <button
              onClick={() =>
                removeCondition(index)
              }
            >
              Remove Condition
            </button>
          )}


          <hr />

        </div>

      ))}


      <button onClick={addCondition}>
        Add Condition
      </button>


      <br />
      <br />


      <button onClick={handleSearch}>
        Search
      </button>


      <h3>Search Results</h3>


      {results.length === 0 ? (
        <p>No results.</p>
      ) : (

        <table border={1}>

          <thead>

            <tr>

              {Object.keys(results[0]).map(
                (column) => (
                  <th key={column}>
                    {column}
                  </th>
                )
              )}

            </tr>

          </thead>


          <tbody>

            {results.map((row, index) => (

              <tr key={index}>

                {Object.values(row).map(
                  (value, valueIndex) => (

                    <td key={valueIndex}>
                      {String(value)}
                    </td>

                  )
                )}

              </tr>

            ))}

          </tbody>

        </table>

      )}

    </div>
  );
}

export default Dashboard;
