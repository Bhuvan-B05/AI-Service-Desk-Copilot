function TicketCard({
    ticket,
    onDelete,
    onAnalyze,
    onResolve,
    loadingAI,
}) {

    const analyzed =
        ticket.ai_summary &&
        ticket.ai_summary !== "AI service temporarily unavailable.";

    return (

        <div className="ticket-card">

            <h3>{ticket.title}</h3>

            <p>{ticket.description}</p>

            <div className="ticket-meta">

                <span
                    className={`status-badge ${ticket.status.toLowerCase()}`}
                >
                    {ticket.status}
                </span>

                <span
                    className={`priority-badge ${(ticket.priority || "Medium").toLowerCase()}`}
                >
                    {ticket.priority || "Medium"}
                </span>

            </div>

            <div className="ticket-actions">

                <button
                    className="analyze-btn"
                    disabled={loadingAI === ticket.id}
                    onClick={() => onAnalyze(ticket.id)}
                >
                    {loadingAI === ticket.id
                        ? "Analyzing..."
                        : analyzed
                        ? "Reanalyze"
                        : "Analyze AI"}
                </button>

                <button
                    className="resolve-btn"
                    onClick={() => onResolve(ticket)}
                >
                    {ticket.status === "Resolved"
                        ? "Reopen"
                        : "Resolve"}
                </button>

                <button
                    className="delete-btn"
                    onClick={() => onDelete(ticket.id)}
                >
                    Delete
                </button>

            </div>

            {!analyzed ? (

                <div className="analysis-box">

                    <h4>AI Analysis</h4>

                    <p>No AI analysis available.</p>

                </div>

            ) : (

                <div className="analysis-box">

                    <h4>AI Analysis</h4>

                    <p>
                        <strong>Category:</strong> {ticket.category}
                    </p>

                    <p>
                        <strong>Priority:</strong> {ticket.priority}
                    </p>

                    <p>
                        <strong>Severity:</strong> {ticket.severity}
                    </p>

                    <p>
                        <strong>Summary:</strong> {ticket.ai_summary}
                    </p>

                    <p>
                        <strong>Root Cause:</strong> {ticket.ai_root_cause}
                    </p>

                    <p>
                        <strong>Resolution:</strong> {ticket.ai_resolution}
                    </p>

                    <p>
                        <strong>Assigned Team:</strong> {ticket.assigned_team}
                    </p>

                    <p>
                        <strong>Estimated Time:</strong> {ticket.estimated_time}
                    </p>

                </div>

            )}

        </div>

    );
}

export default TicketCard;