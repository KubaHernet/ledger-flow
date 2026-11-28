import type { Invoice, InvoiceDraft } from './types'
import { useEffect, useState } from 'react'
import './InvoicesPage.css'
import { InvoiceEditorRow } from './InvoiceEditorRow'
import { getInvoices } from './api'

const emptyInvoiceDraft: InvoiceDraft = {
    number: '',
    amount: '',
    issueDate: '',
    dueDate: '',
    status: 'open',
}

export function InvoicesPage() {
    const [invoices, setInvoices] = useState<Invoice[]>([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [isAdding, setIsAdding] = useState(false)
    const [editingInvoiceId, setEditingInvoiceId] = useState<string | null>(null)

    useEffect(() => {
        const controller = new AbortController()
        const { signal } = controller

        async function loadInvoices() {
            try {
                const data = await getInvoices(signal)

                if (!signal.aborted) {
                    setInvoices(data)
                }
            } catch (error) {
                if (!signal.aborted) {
                    setError(
                        error instanceof Error
                            ? error.message
                            : 'Could not load invoices',
                    )
                }
            } finally {
                if (!signal.aborted) {
                    setIsLoading(false)
                }
            }
        }

        void loadInvoices()

        return () => controller.abort()
    }, [])


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
            {isLoading && <p role="status">Loading invoices…</p>}

            {error && <p role="alert">{error}</p>}

            {!isLoading && !error && invoices.length === 0 && (
                <p>No invoices found.</p>
            )}

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
