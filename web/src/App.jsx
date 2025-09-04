import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [lat, setLat] = useState(47.6);
  const [lon, setLon] = useState(-122.3);
  const [date, setDate] = useState('2025-09-01')
  const [minAlt, setMinAlt] = useState(30) 
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [targets, setTargets] = useState([]);
  const [selected, setSelected] = useState(null);

  const API = 'http://localhost:8000';
  async function fetchTargets() {
    setLoading(true);
    setError("");
    setTargets([]);
    setSelected(null);
    try {
      const url = new URL(`${API}/api/targets`);
      url.searchParams.set("lat", lat);
      url.searchParams.set("lon", lon);
      url.searchParams.set("date", date);
      url.searchParams.set("min_alt", minAlt)

      const res = await fetch(url)
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`API ${res.status}: ${text}`);
      }
      const data = await res.json();
      setTargets(data);
      setSelected(data[0] || null);
    } catch (e) {
      setError(e.message || "Request failed");
    } finally {
      setLoading(false);
    }
  }
  return (
  <div syle={{ maxWidth:900, margin: "20px auto", padding: 12 }}>
    <h1>Zenith - Star Visibility</h1>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: 8, alignItems: "end", margin: "12px 0" }}>
        <label style={{ display: "grid", gap: 4}}>
          <span>Latitude</span>
          <input value={lat} onChange={(e) => setLat(Number(e.target.value))}/>
        </label>

        <label style={{ display: "grid", gap: 4 }}>
          <span>Longitude</span>
          <input value={lon} onChange={(e) => setLon(Number(e.target.value))} />
        </label>

        <label style={{ display: "grid", gap: 4 }}>
          <span>Date (UTC)</span>
          <input value={date} onChange={(e) => setDate(e.target.value)} placeholder="YYYY-MM-DD" />
        </label>

        <label style={{ display: "grid", gap: 4 }}>
          <span>Min Alt (°)</span>
          <input type="number" value={minAlt} onChange={(e) => setMinAlt(Number(e.target.value))} min={0} max={90} />
        </label>

        <button onClick={fetchTargets} style={{ height: 36 }}>
          Search
        </button>
      </div>
      {loading && <p>Loading…</p>}
      {error && <p style={{ color: "crimson" }}>{error}</p>}
      {!loading && !error && targets.length === 0 && <p>No results yet.</p>}
      
      <div style={{ marginTop: 16}}>
        <pre>{JSON.stringify(targets, null, 2)}</pre>
      </div>
  </div>
     );
}

export default App;

// function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <div>
//         <a href="https://vite.dev" target="_blank">
//           <img src={viteLogo} className="logo" alt="Vite logo" />
//         </a>
//         <a href="https://react.dev" target="_blank">
//           <img src={reactLogo} className="logo react" alt="React logo" />
//         </a>
//       </div>
//       <h1>Vite + React</h1>
//       <div className="card">
//         <button onClick={() => setCount((count) => count + 1)}>
//           count is {count}
//         </button>
//         <p>
//           Edit <code>src/App.jsx</code> and save to test HMR
//         </p>
//       </div>
//       <p className="read-the-docs">
//         Click on the Vite and React logos to learn more
//       </p>
//     </>
//   )
// }

// export default App
