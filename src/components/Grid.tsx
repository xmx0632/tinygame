import Cell from './Cell';
import styles from '../styles/Game.module.css';

interface GridProps {
  grid: number[][];
}

export default function Grid({ grid }: GridProps) {
  return (
    <div className={styles.grid}>
      {grid.map((row, i) =>
        row.map((value, j) => (
          <Cell key={`${i}-${j}`} value={value} />
        ))
      )}
    </div>
  );
} 