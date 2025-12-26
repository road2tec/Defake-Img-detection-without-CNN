import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const Navbar = () => {
    const { user, logout } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <nav>
            <div className="nav-logo">TrueFace AI</div>
            <div className="nav-links">
                <Link to="/" className="nav-link">Home</Link>
                <Link to="/features" className="nav-link">Features</Link>

                {user ? (
                    <>
                        <Link to="/history" className="nav-link">History</Link>
                        <button onClick={handleLogout} className="nav-link" style={{ background: 'transparent', padding: 0 }}>
                            Logout
                        </button>
                    </>
                ) : (
                    <>
                        <Link to="/login" className="nav-link">Login</Link>
                        <Link to="/register" className="nav-link">Register</Link>
                    </>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
