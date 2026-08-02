import { useNavigate } from "react-router-dom";

function Navbar() {

    const navigate = useNavigate();

    function logout() {

        localStorage.removeItem("token");

        navigate("/");
    }

    return (

        <nav className="navbar">

            <h2>AI Service Desk Copilot</h2>

            <button onClick={logout}>
                Logout
            </button>

        </nav>

    );
}

export default Navbar;