import React from "react";
import {NavLink} from "react-router-dom";

  function Navigation({onLogout}) {

    function handleLogout() {
      fetch('/api/logout', {
        method: 'DELETE',
      }).then(() => {
        onLogout();  // Call the onLogout prop to handle any state changes
      }).catch(error => {
        console.error('Error during logout:', error);
      });
    }
    return (
      
                  <div className="navBar">
                    <h1 className="navName">Site Name</h1>

                      <div className="navLinks">
                        <NavLink
                        to="/"
                        exact
                        activeStyle={{
                          background: "white",
                        }}
                        >Home</NavLink>
                      </div>
                    

                    <div className="navLinks">
                      <NavLink 
                      to="/create-rides"
                      exact
                      activeStyle={{
                        background: "white",
                      }}
                      >Create Ride</NavLink>
                    </div>

                    
                    <div className="navLinks">
                      <NavLink 
                      to="/my-rides"
                      exact
                      activeStyle={{
                        background: "white",
                      }}
                      >My Rides</NavLink>
                    </div>

                    <div className="navLinks">
                      <NavLink
                      to="/my-bookings"
                      exact
                      activeStyle={{
                        background: "white",
                      }}
                      >My Bookings</NavLink>
                    </div>

                  

                    <div>
                      <button onClick={handleLogout} className="logoutButton">
                        Logout
                      </button>

                    </div>
                </div>
    )
  }

export default Navigation;