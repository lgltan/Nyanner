import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import bP from '../game/pieces/bP.png';

const BrokenPage = () => {
    const [brokenimg] = useState(bP);
    const navigate = useNavigate()

    return (
        <div className='brokenpage-container'
            style={{width: "50%", margin: " 160px auto", textAlign: "center"}}
        >
            <img src={brokenimg} alt="brokenpage" style={{margin: "auto"}}/>
            <h2 style={{margin: "-10px 0 30px 0"}}>Oops... Something went wrong.</h2>
            <button className='primary-btn' onClick={() => navigate('/login')}>Log In</button>
        </div>
    );
}

export default BrokenPage;