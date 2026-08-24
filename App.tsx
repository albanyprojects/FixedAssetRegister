import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";
import Device from "./pages/Device";
import Employee from "./pages/Employee";
import Department from "./pages/Department";
import DeviceType from "./pages/DeviceType";
import AuditLog from "./pages/AuditLog";

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Navbar />

        <main className="content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/Device" element={<Device />} />
            <Route path="/Employee" element={<Employee />} />
            <Route path="/Department" element={<Department />} />
            <Route path="/DeviceType" element={<DeviceType />} />
            <Route path="/AuditLog" element={<AuditLog />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;


