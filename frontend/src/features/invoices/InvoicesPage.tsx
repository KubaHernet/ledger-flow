import type { Invoice, InvoiceDraft } from './types'
import { useState } from 'react'
import './InvoicesPage.css'
import { InvoiceEditorRow } from './InvoiceEditorRow'

const initialInvoices: Invoice[] = [
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

const emptyInvoiceDraft: InvoiceDraft = {
    number: '',
    amount: '',
    issueDate: '',
    dueDate: '',
    status: 'open',
}

export function InvoicesPage() {
    const [invoices, setInvoices] = useState<Invoice[]>(initialInvoices)
    const [isAdding, setIsAdding] = useState(false)
    const [editingInvoiceId, setEditingInvoiceId] = useState<string | null>(null)


    function saveNewInvoice(value: InvoiceDraft) {
        const invoice: Invoice = {
            ...value,
            id: crypto.randomUUID(),
        }

        setInvoices((current) => [...current, invoice])
        setIsAdding(false)
    }

    function saveEditedInvoice(id: string, value: InvoiceDraft) {
        setInvoices((current) =>
            current.map((invoice) =>
                invoice.id === id
                    ? { ...value, id }
                    : invoice,
            ),
        )

        setEditingInvoiceId(null)
    }


    return (
        <main className="invoices-page">
            <h1 className="invoices-page__title">Invoices</h1>

            <button
                type="button"
                onClick={() => setIsAdding(true)}
                disabled={isAdding}
            >
                Add invoice
            </button>
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
                            <th scope="col">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {invoices.map((invoice) =>
                            invoice.id === editingInvoiceId ? (
                                <InvoiceEditorRow
                                    key={invoice.id}
                                    initialValue={invoice}
                                    onSave={(updatedInvoice) => saveEditedInvoice(invoice.id, updatedInvoice)}
                                    onCancel={() => setEditingInvoiceId(null)}
                                />
                            ) : (
                                <tr key={invoice.id}>
                                    <td>{invoice.number}</td>
                                    <td>{invoice.amount}</td>
                                    <td>{invoice.issueDate}</td>
                                    <td>{invoice.dueDate}</td>
                                    <td>{invoice.status}</td>
                                    <td>
                                        <button
                                            type="button"
                                            onClick={() => setEditingInvoiceId(invoice.id)}
                                        >
                                            Edit
                                        </button>
                                    </td>
                                </tr>
                            ),
                        )}
                        {isAdding && (
                            <InvoiceEditorRow
                                key="new-invoice"
                                initialValue={emptyInvoiceDraft}
                                onSave={saveNewInvoice}
                                onCancel={() => setIsAdding(false)}
                            />
                        )}
                    </tbody>
                </table>
            </div>
        </main>
    )
}
