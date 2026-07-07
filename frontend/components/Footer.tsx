export default function Footer() {
  return (
    <footer
      style={{
        marginLeft: "260px",
        marginTop: "40px",
        padding: "24px 32px",
        borderTop: "1px solid #1e293b",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        color: "#94a3b8",
        fontSize: "14px",
      }}
    >
      <div>
        © {new Date().getFullYear()}{" "}
        <span
          className="gradient-text"
          style={{
            fontWeight: 700,
          }}
        >
          DevBrain AI
        </span>
      </div>

      <div
        style={{
          display: "flex",
          gap: "24px",
        }}
      >
        <span>Built with ❤️ using Cognee</span>

        <span>FastAPI</span>

        <span>Next.js</span>

        <span>Neo4j</span>

        <span>Qdrant</span>
      </div>
    </footer>
  );
}