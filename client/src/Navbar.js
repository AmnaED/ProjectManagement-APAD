
import Logout from "./Logout"
function Navbar() {
    return (
        <nav>
            <ul style={{listStyle: 'none', margin: 0, padding: 0, display: 'flex', gap: '20px', alignItems: 'center'}}>
            <li><a href='/'>User Login</a></li>
            <li><a href='/resource-management'>Resource Management</a></li>
            <li><Logout /></li>
            </ul>
        </nav>
    );
}

export default Navbar;
