import type { Invoice } from './types'
import './InvoicesPage.css'

const invoices: Invoice[] = [
    {
        id: '1',
        number: 'INV/2026/001',
        issueDate: '2026-11-01',
        dueDate: '2026-11-30',
        amount: '1234.56',
        status: 'open',
    },
    {
        id: '2',
        number: 'INV/2026/002',
        issueDate: '2026-11-02',
        dueDate: '2026-11-16',
        amount: '2500.00',
        status: 'paid',
    },
]

export function InvoicesPage() {
    return (
        <main className="invoices-page">
            <h1 className="invoices-page__title">Invoices</h1>

            <div className="invoices-page__table-container">
                <table className="invoices-page__table">
                    <caption>All invoices</caption>
                    <thead>
                        <tr>
                            <th scope="col">Number</th>
                            <th scope="col">Amount</th>
                            <th scope="col">Issue date</th>
                            <th scope="col">Due date</th>
                            <th scope="col">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {invoices.map((invoice) => (
                            <tr key={invoice.id}>
                                <td>{invoice.number}</td>
                                <td>{invoice.amount}</td>
                                <td>{invoice.issueDate}</td>
                                <td>{invoice.dueDate}</td>
                                <td>{invoice.status}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </main>
    )
}
