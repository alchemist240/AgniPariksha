import React, { useEffect, useState } from "react";
import "./Tracker.css";

const prompts = [
  "What's your favorite color?",
  "Pizza or Burger?",
  "Favorite movie?",
  "A dream travel destination?",
  "What's your favorite hobby?",
  "Tea or Coffee?",
  "Morning person or night owl?",
  "Books or movies?",
  "Rainy days or sunny days?",
  "What’s your go-to comfort food?",
  "Mountains or beaches?",
  "Which season do you like the most?",
  "What’s your favorite board game?",
  "Cats or dogs?"
];

const generateNonce = () => {
  return Math.random().toString(36).substring(2) + Date.now().toString(36);
};

const Tracker = () => {
  const [prompt, setPrompt] = useState("");
  const [answer, setAnswer] = useState("");
  const [startTime, setStartTime] = useState(null);
  const [keystrokes, setKeystrokes] = useState([]);
  const [mouseMovements, setMouseMovements] = useState([]);
  const [nonce, setNonce] = useState("");
  const [status, setStatus] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isBot, setIsBot] = useState(false); // ✅ Simulate Bot toggle state

  useEffect(() => {
    initializeTracker();

    const handleMouseMove = (e) => {
      const timestamp = Date.now() - startTime;
      const { clientX, clientY } = e;
      setMouseMovements((prev) => [...prev, { x: clientX, y: clientY, time: timestamp }]);
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  const initializeTracker = () => {
    setPrompt(prompts[Math.floor(Math.random() * prompts.length)]);
    setStartTime(Date.now());
    setNonce(generateNonce());
  };

  const resetTracker = () => {
    setPrompt(prompts[Math.floor(Math.random() * prompts.length)]);
    setStartTime(Date.now());
    setKeystrokes([]);
    setMouseMovements([]);
    setAnswer("");
    setNonce(generateNonce());
    setPrediction(null);
    setStatus("");
    setIsSubmitting(false);
  };

  const handleKeyDown = (e) => {
    const timestamp = Date.now() - startTime;
    setKeystrokes((prev) => [...prev, { key: e.key, time: timestamp }]);

    const keyElem = document.getElementById(`key-${e.key.toLowerCase()}`);
    if (keyElem) {
      keyElem.classList.add("glow");
      setTimeout(() => keyElem.classList.remove("glow"), 300);
    }
  };

  const calculateFeatures = () => {
    const reaction_time = Date.now() - startTime;
    const answer_length = answer.length;

    const intervals = [];
    for (let i = 1; i < keystrokes.length; i++) {
      intervals.push(keystrokes[i].time - keystrokes[i - 1].time);
    }

    const avg_key_interval =
      intervals.length > 0
        ? intervals.reduce((a, b) => a + b, 0) / intervals.length
        : 0;

    const std_key_interval = Math.sqrt(
      intervals.reduce((sum, val) => sum + Math.pow(val - avg_key_interval, 2), 0) /
      (intervals.length || 1)
    );

    let mouse_distance = 0;
    for (let i = 1; i < mouseMovements.length; i++) {
      const dx = mouseMovements[i].x - mouseMovements[i - 1].x;
      const dy = mouseMovements[i].y - mouseMovements[i - 1].y;
      mouse_distance += Math.sqrt(dx * dx + dy * dy);
    }

    const total_time = mouseMovements.length > 0 ? mouseMovements[mouseMovements.length - 1].time : 1;
    const mouse_avg_speed = mouse_distance / total_time;
    const mouse_movements = mouseMovements.length;

    return {
      reaction_time,
      answer_length,
      avg_key_interval,
      std_key_interval,
      mouse_distance,
      mouse_avg_speed,
      mouse_movements
    };
  };

  const handleSubmit = async () => {
    if (!answer.trim()) {
      setStatus("⚠️ Please enter an answer before submitting.");
      return;
    }

    setIsSubmitting(true);

    const payload = {
      prompt,
      answer,
      reaction_time: Date.now() - startTime,
      keystrokes,
      mouseMovements,
      nonce
    };

    try {
      const res = await fetch("http://localhost:5000/api/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      await res.json(); // we don't use its message anymore


      const features = calculateFeatures();

      const predictRes = await fetch("http://localhost:5000/api/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(features)
      });

      const predictResult = await predictRes.json();
      setPrediction(predictResult);

      if (predictResult.label === "human") {
        setStatus("✅ You're verified as human!");
      } else {
        setStatus("🤖 Bot-like behavior detected! Access Denied");
      }


    } catch (err) {
      console.error(err);
      setStatus("❌ Submission failed.");
    }

    setIsSubmitting(false);
  };

  // ✅ Simulate bot answer (just fill text field and state — NO auto submit)
  const handleBotToggle = (checked) => {
    setIsBot(checked);

    if (checked) {
      const botAnswer = "yes";
      const simulatedKeystrokes = botAnswer.split("").map((char, i) => ({
        key: char,
        time: i * 10
      }));

      const simulatedMouse = Array.from({ length: 10 }, (_, i) => ({
        x: 100 + i * 5,
        y: 100 + i * 2,
        time: i * 5
      }));

      setAnswer(botAnswer);
      setKeystrokes(simulatedKeystrokes);
      setMouseMovements(simulatedMouse);
      setStatus("🤖 Simulated bot input. You can now submit.");
    }
  };

  const renderKeyboard = () => {
    const keys = "qwertyuiopasdfghjklzxcvbnm".split("");
    return (
      <div className="keyboard">
        {keys.map((k) => (
          <div key={k} id={`key-${k}`} className="key">
            {k}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="tracker-container">
      <h2>{prompt}</h2>
      <input
        type="text"
        className="input-box"
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your answer..."
      />
      {renderKeyboard()}

      <button
        className="submit-button"
        onClick={handleSubmit}
        disabled={isSubmitting}
      >
        ✅ Submit
      </button>

      <div style={{ marginTop: "10px" }}>
        <label>
          🤖 Simulate Bot:
          <input
            type="checkbox"
            checked={isBot}
            onChange={(e) => handleBotToggle(e.target.checked)}
            style={{ marginLeft: "10px" }}
          />
        </label>
      </div>

      <div className="status" style={{ color: prediction?.label === "bot" ? "red" : "limegreen" }}>
        {status}
      </div>
      {prediction && (
        <div className="prediction">
          🧠 <strong>{prediction.label.toUpperCase()}</strong> <br />
          🔍 Confidence: <strong>{(prediction.confidence * 100).toFixed(2)}%</strong>
        </div>
      )}
      <div className="nonce">Nonce: {nonce}</div>
    </div>
  );
};

export default Tracker;
