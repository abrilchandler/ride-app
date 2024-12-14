import { Link } from "react-router-dom";

function Header({ user }) {
  console.log(user)
  return (
    <header>
      {user ? (
        <div>
          <p>Welcome, {user.username}!</p>
        </div>
      ) : (
        <Link to="/login">Click Here to Login</Link>
      )}
    </header>
  );
}

export default Header;