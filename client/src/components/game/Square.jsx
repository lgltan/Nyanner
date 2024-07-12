const Square = ({ index, piece, onDragStart, onDragEnd, onDrop }) => {
    const handleMouseDown = (e) => {
      e.preventDefault(); // Prevent text selection during drag start
      onDragStart(index); // Assuming index is passed to identify the square being dragged
    };
  
    const handleMouseUp = () => {
      onDragEnd();
    };
  
    const handleMouseMove = (e) => {
      e.preventDefault(); // Prevent text selection during drag
      onDragEnd(); // Assuming this is called to update the visual representation of the board
    };
  
    const handleDragOver = (e) => {
      e.preventDefault(); // Necessary for dropping
      e.dataTransfer.dropEffect = 'move'; // Indicates that the dragged item can be moved
    };
  
    return (
      <div
        className={`square ${piece ? 'occupied' : ''}`}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onDragOver={handleDragOver}
        draggable={!!piece}
      >
        {piece ? piece : ''}
      </div>
    );
  };
  
  export default Square; // Add this line to export the Square component
  