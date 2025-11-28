import React from 'react';
import Navbar from '../ui/Navbar';
import Sidebar from '../components/ui/Sidebar';

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div
      style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}
    >
      <Navbar />
      <main className="app-container" style={{ flex: 1 }}>
        <div
          style={{
            borderLeft: '1px solid rgba(0,0,0,0.04)',
            borderRight: '1px solid rgba(0,0,0,0.04)',
            padding: '24px',
            borderRadius: 8,
          }}
        >
          {children}
        </div>
      </main>
    </div>
  );
}
