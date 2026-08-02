import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";

function Login() {
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        const token = localStorage.getItem("token");

        if (token) {
            navigate("/dashboard");
        }
    }, [navigate]);

    async function handleLogin(e) {
        e.preventDefault();

        setError("");

        try {
            const form = new URLSearchParams();

            form.append("username", email);
            form.append("password", password);

            const response = await api.post(
                "/login",
                form,
                {
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                }
            );

            localStorage.setItem(
                "token",
                response.data.access_token
            );

            navigate("/dashboard");

        } catch (err) {
            setError(
                err.response?.data?.detail || "Login failed."
            );
        }
    }

    return (
        <div className="auth-container">

            <form className="auth-card" onSubmit={handleLogin}>

                <h1>AI Service Desk Copilot</h1>

                <h2>Welcome Back</h2>

                {error && (
                    <p className="error">{error}</p>
                )}

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
                    Login
                </button>

                <p>
                    Don't have an account?{" "}
                    <Link to="/register">
                        Register
                    </Link>
                </p>

            </form>

        </div>
    );
}

export default Login;