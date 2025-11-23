import React from 'react';
import styles from '../../styles/components/button.module.css';

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'danger';
};

export default function Button({
  variant = 'primary',
  children,
  ...rest
}: ButtonProps) {
  return (
    <button className={`${styles.btn} ${styles[variant]}`} {...rest}>
      {children}
    </button>
  );
}
