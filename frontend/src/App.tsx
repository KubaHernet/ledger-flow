import { Navigate, Route, Routes } from "react-router"
import { InvoicesPage } from "./features/invoices/InvoicesPage"

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/invoices" replace />} />
      <Route path="/invoices" element={<InvoicesPage />} />
      <Route path="*" element={<h1>Page not found</h1>} />
    </Routes>
  )
}

export default App