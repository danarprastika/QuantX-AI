import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <div className="min-h-screen bg-white">
      <Routes>
        <Route path="/" element={<div>QuantX AI</div>} />
      </Routes>
    </div>
  );
}

export { App };
