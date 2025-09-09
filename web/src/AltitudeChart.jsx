import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid,
    ReferenceLine,
} from 'recharts';
import { useMemo } from 'react';

/**
 * AltitudeChart
 * Props:
 *  - series: Array<{ t: string, alt_deg: number }>
 *  - minAlt: number (threshold line)
 */
export default function AltitudeChart({ series, minAlt = 30 }) {
    // normalize data for recharts
    const data = useMemo(() => {
        if (!Array.isArray(series)) return [];
        return series.map(p => ({
            time: p.t,
            altitude: Math.round(p.alt_deg * 10) / 10, // round to 0.1 deg
        }));
    }, [series]);

    if (!data.length) {
        return <p style = {{ fontSize: 12, color: "#666" }}>No data to plot.</p>;
    }
    
    return (
        <div aria-label='Altitude over time'>
        <ResponsiveContainer width="100%" height={340}>
            <LineChart data={data} margin={{ top: 10, right: 24, bottom: 36, left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                    dataKey="time"
                    tickFormatter={safeHHMM}
                    tickMargin={8}
                    label={{ value: 'Time (UTC)', position: 'insideBottom', offset: -20 }}
                />
                <YAxis 
                    domain={[0, 90]}
                    tickCount={8}
                    label={{ value: 'Altitude (°)', angle: -90, position: 'insideLeft'}}
                />
                <Tooltip
                    labelFormatter={(_value, _payload, idx) => data[idx]?.iso || ""}
                    formatter={(v, k) => (k === "alt" ? [`${format1(v)}°`, "Altitude"] : [v, k])}
                />
                <ReferenceLine 
                    y={minAlt} 
                    strokeDasharray="4 4" 
                    stroke='red'
                />
                <Line
                    type="monotone"
                    dataKey="altitude"
                    dot={false}
                    isAnimationActive={false}
                    connectNulls
                />
                </LineChart>
            </ResponsiveContainer>
            <p style={{ fontSize: 12, color: "#666", marginTop: 8 }}>
                Colored <b>horizontal</b> line shows minimum altitude threshold ({minAlt}°).
            </p>
        </div>
    );
}

function safeHHMM(iso) {
    try {
        return new Date(iso).toISOString().slice(11, 16);
    } catch {
        return iso;
    }
}

function format1(n) {
    if (typeof n !== 'number' || Number.isNaN(n)) return '-';
    return n.toFixed(1);
}