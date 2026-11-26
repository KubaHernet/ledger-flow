import { useState } from "react"
import type { InvoiceDraft } from "./types"

type InvoiceEditorRowProps = {
    initialValue: InvoiceDraft
    onSave: (value: InvoiceDraft) => void
    onCancel: () => void
}

export function InvoiceEditorRow({
    initialValue,
    onSave,
    onCancel
}: InvoiceEditorRowProps) {
    const [draft, setDraft] = useState<InvoiceDraft>(initialValue)

    function updateField<K extends keyof InvoiceDraft>(
        field: K,
        value: InvoiceDraft[K],
    ) {
        setDraft((current) => ({ ...current, [field]: value }))
    }

    return (
        <tr>
            <td>
                <input
                    aria-label="Invoice number"
                    value={draft.number}
                    onChange={(event) =>
                        updateField('number', event.target.value)
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
                        updateField('amount', event.target.value)
                    }
                />
            </td>
            <td>
                <input
                    aria-label="Issue date"
                    type="date"
                    value={draft.issueDate}
                    onChange={(event) =>
                        updateField('issueDate', event.target.value)
                    }
                />
            </td>
            <td>
                <input
                    aria-label="Due date"
                    type="date"
                    value={draft.dueDate}
                    onChange={(event) =>
                        updateField('dueDate', event.target.value)
                    }
                />
            </td>
            <td>{draft.status}</td>
            <td>
                <button type="button" onClick={() => onSave(draft)}>
                    Save
                </button>
                <button type="button" onClick={onCancel}>
                    Cancel
                </button>
            </td>
        </tr>
    )
}