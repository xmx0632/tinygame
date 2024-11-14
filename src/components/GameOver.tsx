import styles from '../styles/Game.module.css';

interface GameOverProps {
  onReset: () => void;
}

export default function GameOver({ onReset }: GameOverProps) {
  return (
    <div className={styles.gameOver}>
      <h2>Game Over!</h2>
      <button className={styles.button} onClick={onReset}>
        Try Again
      </button>
    </div>
  );
} 