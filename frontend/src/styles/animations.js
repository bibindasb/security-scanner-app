// frontend/src/styles/animations.js
export const animations = {
  fadeIn: {
    animation: 'fadeIn 0.5s ease-in',
  },
  slideIn: {
    animation: 'slideIn 0.3s ease-out',
  },
  pulse: {
    animation: 'pulse 2s infinite',
  },
};

// Add to your global CSS
export const animationStyles = `
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes slideIn {
    from { transform: translateY(-20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }
  
  @keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
  }
`;