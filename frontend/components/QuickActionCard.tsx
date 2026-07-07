"use client";

type QuickActionCardProps = {
  icon: string;
  title: string;
  description: string;
  color: string;
  onClick?: () => void;
};

export default function QuickActionCard({
  icon,
  title,
  description,
  color,
  onClick,
}: QuickActionCardProps) {
  return (
    <div
      onClick={onClick}
      style={{
        position: "relative",
        overflow: "hidden",
        background: "#111827",
        border: "1px solid #1f2937",
        borderRadius: 22,
        padding: 28,
        cursor: "pointer",
        transition: "all .25s ease",
        boxShadow: "0 12px 30px rgba(0,0,0,.25)",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "translateY(-8px)";
        e.currentTarget.style.borderColor = color;
        e.currentTarget.style.boxShadow =
          `0 20px 40px ${color}25`;
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "translateY(0)";
        e.currentTarget.style.borderColor = "#1f2937";
        e.currentTarget.style.boxShadow =
          "0 12px 30px rgba(0,0,0,.25)";
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
          width: 70,
          height: 70,
          borderRadius: "50%",
          background: `${color}20`,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          fontSize: 34,
          marginBottom: 24,
        }}
      >
        {icon}
      </div>

      {/* Title */}

      <h2
        style={{
          color: "#ffffff",
          fontSize: 24,
          fontWeight: 700,
          marginBottom: 12,
        }}
      >
        {title}
      </h2>

      {/* Description */}

      <p
        style={{
          color: "#94a3b8",
          lineHeight: 1.7,
          fontSize: 15,
          marginBottom: 22,
        }}
      >
        {description}
      </p>

      {/* Footer */}

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <span
          style={{
            color,
            fontWeight: 700,
            fontSize: 14,
          }}
        >
          Explore
        </span>

        <div
          style={{
            width: 36,
            height: 36,
            borderRadius: "50%",
            background: `${color}20`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color,
            fontSize: 18,
            fontWeight: "bold",
          }}
        >
          →
        </div>
      </div>
    </div>
  );
}