import type { Invoice } from './types'
import { useState } from 'react'
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

type InvoiceDraft = Omit<Invoice, 'id'>

export function InvoicesPage() {
    const [draft, setDraft] = useState<InvoiceDraft | null>(null)

    function addInvoice() {
        setDraft({
            number: '',
            amount: '',
            issueDate: '',
            dueDate: '',
            status: 'open',
        })
    }

    function saveNewInvoice() {
        if(draft == null)
            return;

        var invoice: Invoice = { ...draft, id: invoices.length.toString() }
        invoices.push(invoice)

        setDraft(null)
    }

    function updateDraft<K extends keyof InvoiceDraft>(
        field: K,
        value: InvoiceDraft[K],
    ) {
        setDraft((current) =>
            current ? { ...current, [field]: value } : null,
        )
    }


    return (
        <main className="invoices-page">
            <h1 className="invoices-page__title">Invoices</h1>

            <button
                type="button"
                onClick={addInvoice}
                disabled={draft !== null}
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
                        {invoices.map((invoice) => (
                            <tr key={invoice.id}>
                                <td>{invoice.number}</td>
                                <td>{invoice.amount}</td>
                                <td>{invoice.issueDate}</td>
                                <td>{invoice.dueDate}</td>
                                <td>{invoice.status}</td>
                                <td />
                            </tr>
                        ))}
                        {draft && (
                            <tr>
                                <td>
                                    <input
                                        aria-label="Invoice number"
                                        value={draft.number}
                                        onChange={(event) =>
                                            updateDraft('number', event.target.value)
                                        }
                                    />
                                </td>
                                <td>
                                    <input
                                        aria-label="Amount"
                                        type="number"
                                        min="0.01"
                                        step="0.01"
                                        value={draft.amount}
                                        onChange={(event) =>
                                            updateDraft('amount', event.target.value)
                                        }
                                    />
                                </td>
                                <td>
                                    <input
                                        aria-label="Issue date"
                                        type="date"
                                        value={draft.issueDate}
                                        onChange={(event) =>
                                            updateDraft('issueDate', event.target.value)
                                        }
                                    />
                                </td>
                                <td>
                                    <input
                                        aria-label="Due date"
                                        type="date"
                                        value={draft.dueDate}
                                        onChange={(event) =>
                                            updateDraft('dueDate', event.target.value)
                                        }
                                    />
                                </td>
                                <td>Open</td>
                                <td>
                                    <button type="button" onClick={() => saveNewInvoice()}>
                                        Save
                                    </button>
                                    <button type="button" onClick={() => setDraft(null)}>
                                        Cancel
                                    </button>
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </main>
    )
}
