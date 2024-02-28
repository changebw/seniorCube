import React from "react";
import "./Navbar.css"
import {Link} from 'react-router-dom';

const Navbar=()=>{
    return (
        <div className="Navbar">
            <div>
                <Link className="NavbarLink first" to="/">
                    <h3 className="NavbarLink-title">Solve</h3>
                </Link>
            </div>
            <div className="">
                <Link className="NavbarLink" to="/race">
                    <h3 className="NavbarLink-title">Race</h3>
                </Link>
            </div>
            <div className="">
                <Link className="NavbarLink" to="/learn">
                    <h3 className="NavbarLink-title">Learn</h3>
                </Link>
            </div>
            <div className="">
                <Link className="NavbarLink last" to="/about">
                    <h3 className="NavbarLink-title">About Us</h3>
                </Link>
            </div>
        </div>
    )
}

export default Navbar;