import { useState } from 'react'
import './App.css'

const API = 'http://localhost:8000';

function App() {
  const [lat, setLat] = useState("47.6");
  const [lon, setLon] = useState("-122.3");
  const [date, setDate] = useState("2025-09-01")
  const [minAlt, setMinAlt] = useState("30") 
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [targets, setTargets] = useState([]);
  const [selected, setSelected] = useState(null);

  async function fetchTargets() {
    const latNum = parseFloat(lat);
    const lonNum = parseFloat(lon);
    const minAltNum = parseFloat(minAlt);

    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) {
      setError("Date must be YYYY-MM-DD");
      return;
    }
    if (lat.trim() === "" || Number.isNaN(latNum) || latNum < -90 || latNum > 90) {
      setError("Latitude must be a number between -90 and 90");
      return;
    }
    if (lon.trim() === "" || Number.isNaN(lonNum) || lonNum < -180 || lonNum > 180) {
      setError("Longitude must be a number between -180 and 180");
      return;
    }
    if (minAlt.trim() === "" || Number.isNaN(minAltNum) || minAltNum < 0 || minAltNum > 90) {
      setError("Min Alt must be a number between 0 and 90");
      return;
    }

    setLoading(true);
    setError("");
    setTargets([]);
    setSelected(null);
     
    try {
      const url = new URL(`${API}/api/targets`);
      url.searchParams.set("lat", String(lat));
      url.searchParams.set("lon", String(lon));
      url.searchParams.set("date", date);
      url.searchParams.set("min_alt", String(minAlt))

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
  
  function renderRow(t, i) {
    const peak = 
      typeof t.peak_altitude_deg === "number"
        ? t.peak_altitude_deg.toFixed(1)
        : "-";
    
    const win = t.best_window
      ? `${t.best_window.start} -> ${t.best_window.end}`
      : "-"
    
    const isSelected = selected?.name === t.name;

    return(
      <tr
        key={t.name + i}
        onClick={() => setSelected(t)}
        className={isSelected ? "selected" : ""}
        style={{ cursor: "pointer" }}
      >
        <td className="cell">{t.name}</td>
        <td className="cell">{t.vmag ?? "—"}</td>
        <td className="cell">{peak}</td>
        <td className="cell window">{win}</td>
      </tr>
    )
  }

  function hhmm(iso) {
    try {
      return new Date(iso).toISOString().slice(11, 16);
    } catch {
      return iso;
    }
  }
  return (
  <div style={{ maxWidth:900, margin: "20px auto", padding: 12 }}>
    <h1>Zenith - Star Visibility</h1>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: 8, alignItems: "end", margin: "12px 0" }}>
        <label style={{ display: "grid", gap: 4}}>
          <span>Latitude</span>
          <input 
            value={lat} 
            onChange={(e) => setLat(e.target.value)}
            inputMode="decimal"
            placeholder='e.g. 47.6'
          />
        </label>

        <label style={{ display: "grid", gap: 4 }}>
          <span>Longitude</span>
          <input 
            value={lon} 
            onChange={(e) => setLon(e.target.value)} 
            inputMode='decimal' 
            placeholder='e.g. -122.3'
            />
        </label>

        <label style={{ display: "grid", gap: 4 }}>
          <span>Date (UTC)</span>
          <input value={date} onChange={(e) => setDate(e.target.value)} placeholder="YYYY-MM-DD" />
        </label>

        <label style={{ display: "grid", gap: 4 }}>
          <span>Min Alt (°)</span>
          <input 
            type="number" 
            step='any'
            value={minAlt} 
            placeholder='eg. 40'
            min={0} 
            max={90} 
            onChange={(e) => setMinAlt(e.target.value)} 
            />
        </label>

        <button onClick={fetchTargets} disabled={loading} style={{ height: 36 }}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>
      {loading && <p>Loading…</p>}
      {error && <p style={{ color: "crimson" }}>{error}</p>}
      {!loading && !error && targets.length === 0 && <p>No results yet.</p>}
      {targets.length > 0 && !loading && !error && (
        <p style={{ marginTop: 8}}>
          Found {targets.length} targets - click a row to preview
        </p>
      )} 

      {targets.length > 0 && (
        <div style={{ overflowX: "auto", marginTop: 8}}>
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Vmag</th>
                <th>Peak Alt</th>
                <th>Best Window (UTC)</th>
              </tr>
            </thead>
            <tbody>{targets.map(renderRow)}</tbody>
          </table>
        </div>
      )}

      {selected && (
        <div style={{ marginTop: 16 }}>
          <h3>Altitude series — {selected.name}</h3>
          <p style={{ fontSize: 12, color: "#555" }}>
            First 5 points:&nbsp;
            {selected.series
              .slice(0, 5)
              .map((p) => `${hhmm(p.t)}=${Math.round(p.alt_deg)}°`)
              .join(", ")}
          </p>
        </div>
      )}

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
