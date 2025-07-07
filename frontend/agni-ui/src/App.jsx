import React from "react";
import Tracker from "./components/Tracker";

function App() {
  return (
    <div
      style={{
        height: "100vh",
        width: "100vw",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#0a0a0a",
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        color: "#f5f5f5",
        padding: "2rem",
      }}
    >
      <div style={{ textAlign: "center", maxWidth: "700px", width: "100%" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "0.5rem" }}>🔥 AgniPariksha 🔥</h1>
        <p style={{ color: "#999", marginBottom: "2rem" }}>
          Proving you're human through behavior...
        </p>
        <Tracker />
      </div>
    </div>
  );
}

export default App;
