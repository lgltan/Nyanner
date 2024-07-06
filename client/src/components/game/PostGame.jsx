// match logs and placement
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const PostGame = () => {
  const [Ranking, setRanking] = useState([]);

  useEffect(() => {
    const fetchRanking = async () => {
      try {
        const res = await axios.get('API ENDPOINT FOR GAME TABLE');
        let ranking = [0,0,0,0]
        ranking[res.data.p1_pos] = res.data.p1_id
        ranking[res.data.p2_pos] = res.data.p2_id
        ranking[res.data.p3_pos] = res.data.p3_id
        ranking[res.data.p4_pos] = res.data.p4_id
        
        // check if all ranks were returned correctly
        if (ranking.includes(0)) throw "Failed to fetch ranking.";

        setRanking(ranking);
      } catch (error) {
        console.error("Failed to fetch ranking:", error);
      }
    };

    fetchRanking();
  }, []);

  return (
    <div>
      <h2>Game Summary</h2>
      <ul>
        {Ranking.map((player, index) => (
          <li key={index}>{`${index + 1}. ${player.name}`}</li>
        ))}
      </ul>
    </div>
  );
};

export default PostGame;
