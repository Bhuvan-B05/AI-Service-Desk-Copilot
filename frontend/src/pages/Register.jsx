import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";

function Register() {
    const navigate = useNavigate();

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    async function handleRegister(e) {
        e.preventDefault();

        setError("");

        try {
            await api.post("/register", {
                name,
                email,
                password,
            });

            navigate("/");

        } catch (err) {
            setError(
                err.response?.data?.detail || "Registration failed."
            );
        }
    }

    return (
        <div className="auth-container">
            <form className="auth-card" onSubmit={handleRegister}>

                <h1>AI Service Desk Copilot</h1>

                <h2>Create Account</h2>

                {error && <p className="error">{error}</p>}

                <input
                    type="text"
                    placeholder="Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />

                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                <button type="submit">
                    Register
                </button>

                <p>
                    Already have an account?{" "}
                    <Link to="/">Login</Link>
                </p>

            </form>
        </div>
    );
}

export default Register;