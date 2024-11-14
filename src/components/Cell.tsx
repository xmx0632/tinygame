import styles from '../styles/Game.module.css';

interface CellProps {
  value: number;
}

export default function Cell({ value }: CellProps) {
  return (
    <div className={`${styles.cell} ${styles[`value${value}`]}`}>
      {value !== 0 ? value : ''}
    </div>
  );
} 