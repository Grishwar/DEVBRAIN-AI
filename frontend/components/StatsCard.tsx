type StatsCardProps = {
  title: string;
  value: string | number;
  icon: string;
  color?: string;
  trend?: string;
};

export default function StatsCard({
  title,
  value,
  icon,
  color = "#3b82f6",
  trend,
}: StatsCardProps) {
  return (
    <div
      style={{
        position: "relative",
        overflow: "hidden",
        background: "#111827",
        border: "1px solid #1f2937",
        borderRadius: 20,
        padding: 24,
        transition: "all .25s ease",
        cursor: "pointer",
        boxShadow: "0 10px 25px rgba(0,0,0,.25)",
      }}
    >
      {/* Top Accent */}

      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: 4,
          background: color,
        }}
      />

      {/* Icon */}

      <div
        style={{
          width: 58,
          height: 58,
          borderRadius: "50%",
          background: `${color}20`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 28,
          marginBottom: 18,
        }}
      >
        {icon}
      </div>

      {/* Title */}

      <div
        style={{
          color: "#94a3b8",
          fontSize: 15,
          fontWeight: 500,
          marginBottom: 10,
        }}
      >
        {title}
      </div>

      {/* Value */}

      <div
        style={{
          fontSize: 38,
          fontWeight: 800,
          color,
          letterSpacing: "-1px",
        }}
      >
        {value}
      </div>

      {/* Trend */}

      {trend && (
        <div
          style={{
            marginTop: 18,
            display: "inline-flex",
            alignItems: "center",
            gap: 6,
            padding: "6px 12px",
            borderRadius: 999,
            background: "#0b1220",
            border: "1px solid #1e293b",
            color: "#22c55e",
            fontSize: 13,
            fontWeight: 600,
          }}
        >
          📈 {trend}
        </div>
      )}
    </div>
  );
}