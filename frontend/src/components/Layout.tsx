import React from 'react';
import { Container } from 'react-bootstrap';
import '../App.css';

const Layout = ({ children }: { children: React.ReactNode }) => (
  <div className="bg-dark text-light min-vh-100 d-flex flex-column">
    <Container className="py-4 flex-grow-1">
      {children}
    </Container>
  </div>
);

export default Layout;
