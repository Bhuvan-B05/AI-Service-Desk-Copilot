import { useEffect, useState } from "react";

import api from "../services/api";
import Navbar from "../components/Navbar";
import TicketCard from "../components/TicketCard";

function Dashboard() {

    const [tickets, setTickets] = useState([]);

    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");

    const [loadingAI, setLoadingAI] = useState(null);
    const [creating, setCreating] = useState(false);

    const [stats, setStats] = useState({});

    const [search, setSearch] = useState("");

    const [statusFilter, setStatusFilter] = useState("All");

    const [priorityFilter, setPriorityFilter] = useState("All");

    const [sortOrder, setSortOrder] = useState("Newest");

    useEffect(() => {
        loadTickets();
        loadDashboard();
    }, []);

    async function loadTickets() {
        try {
            const response = await api.get("/tickets");
            setTickets(response.data);
        } catch (err) {
            console.log(err);
        }
    }

    async function loadDashboard() {
        try {
            const response = await api.get("/dashboard");
            setStats(response.data);
        } catch (err) {
            console.log(err);
        }
    }

    async function createTicket(e) {
        e.preventDefault();

        try {

            setCreating(true);

            await api.post("/tickets", {
                title,
                description,
            });

            setTitle("");
            setDescription("");

            await loadTickets();
            await loadDashboard();

        } catch (err) {

            console.log(err);

        } finally {

            setCreating(false);

        }
    }

    async function deleteTicket(id) {

        if (!window.confirm("Delete this ticket?")) {
            return;
        }

        try {

            await api.delete(`/tickets/${id}`);

            await loadTickets();
            await loadDashboard();

        } catch (err) {
            console.log(err);
        }
    }

    async function analyzeTicket(id) {

        try {

            setLoadingAI(id);

            await api.post(`/tickets/${id}/analyze`);

            await loadTickets();
            await loadDashboard();

        } catch (err) {

            console.log(err);

        } finally {

            setLoadingAI(null);

        }
    }

    async function resolveTicket(ticket) {

        try {

            const newStatus =
                ticket.status === "Resolved"
                    ? "Open"
                    : "Resolved";

            await api.put(`/tickets/${ticket.id}`, {
                status: newStatus,
            });

            await loadTickets();
            await loadDashboard();

        } catch (err) {
            console.log(err);
        }
    }

    const filteredTickets = tickets
        .filter((ticket) => {

            const matchesSearch =
                ticket.title
                    .toLowerCase()
                    .includes(search.toLowerCase()) ||

                ticket.description
                    .toLowerCase()
                    .includes(search.toLowerCase());

            const matchesStatus =
                statusFilter === "All" ||
                ticket.status === statusFilter;

            const matchesPriority =
                priorityFilter === "All" ||
                ticket.priority === priorityFilter;

            return (
                matchesSearch &&
                matchesStatus &&
                matchesPriority
            );

        })
        .sort((a, b) => {

            if (sortOrder === "Newest") {
                return (
                    new Date(b.created_at) -
                    new Date(a.created_at)
                );
            }

            return (
                new Date(a.created_at) -
                new Date(b.created_at)
            );

        });

    return (
        <>
            <Navbar />

            <div className="dashboard">

                <h1>Dashboard</h1>

                <br />

                <div className="stats">

                    <div className="stat-card">
                        <h2>{stats.total_tickets || 0}</h2>
                        <p>Total Tickets</p>
                    </div>

                    <div className="stat-card">
                        <h2>{stats.open_tickets || 0}</h2>
                        <p>Open</p>
                    </div>

                    <div className="stat-card">
                        <h2>{stats.resolved_tickets || 0}</h2>
                        <p>Resolved</p>
                    </div>

                    <div className="stat-card">
                        <h2>{stats.high_priority || 0}</h2>
                        <p>High Priority</p>
                    </div>

                </div>

                <div className="toolbar">

                    <input
                        type="text"
                        placeholder="Search tickets..."
                        value={search}
                        onChange={(e) =>
                            setSearch(e.target.value)
                        }
                    />

                    <select
                        value={statusFilter}
                        onChange={(e) =>
                            setStatusFilter(e.target.value)
                        }
                    >
                        <option>All</option>
                        <option>Open</option>
                        <option>Resolved</option>
                    </select>

                    <select
                        value={priorityFilter}
                        onChange={(e) =>
                            setPriorityFilter(e.target.value)
                        }
                    >
                        <option>All</option>
                        <option>Critical</option>
                        <option>High</option>
                        <option>Medium</option>
                        <option>Low</option>
                    </select>

                    <select
                        value={sortOrder}
                        onChange={(e) =>
                            setSortOrder(e.target.value)
                        }
                    >
                        <option>Newest</option>
                        <option>Oldest</option>
                    </select>

                </div>

                <form
                    className="ticket-form"
                    onSubmit={createTicket}
                >

                    <h2>Create Ticket</h2>

                    <input
                        type="text"
                        placeholder="Ticket Title"
                        value={title}
                        onChange={(e) =>
                            setTitle(e.target.value)
                        }
                        required
                    />

                    <textarea
                        placeholder="Describe the issue..."
                        value={description}
                        onChange={(e) =>
                            setDescription(e.target.value)
                        }
                        required
                    />

                    <button
                        type="submit"
                        disabled={creating}
                    >
                        {creating ? "Creating..." : "Create Ticket"}
                    </button>

                </form>

                <br />

                {filteredTickets.length === 0 ? (

                    <p>No matching tickets found.</p>

                ) : (

                    filteredTickets.map((ticket) => (

                        <TicketCard
                            key={ticket.id}
                            ticket={ticket}
                            onDelete={deleteTicket}
                            onAnalyze={analyzeTicket}
                            onResolve={resolveTicket}
                            loadingAI={loadingAI}
                        />

                    ))

                )}

            </div>

        </>
    );
}

export default Dashboard;