import '../App.css';

const Layout = ({ children }: { children: React.ReactNode }) => (
  <div className="bg-dark text-light min-vh-100">
    <div className="container py-4">{children}</div>
  </div>
);

export default Layout;
