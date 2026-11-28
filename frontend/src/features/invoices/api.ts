import type { Invoice } from './types';


type InvoiceApiItem = {
  invoice_id: string
  invoice_number: string
  issue_date: string
  due_date: string
  amount: string
  status: Invoice['status']
}


type GetInvoicesResponse = {
  invoices: InvoiceApiItem[]
}

export async function getInvoices(
  signal?: AbortSignal,
): Promise<Invoice[]> {
  const response = await fetch('/api/invoices', { signal })

  if (!response.ok) {
    throw new Error(`Could not load invoices (${response.status})`)
  }

  const data: GetInvoicesResponse = await response.json()

  return data.invoices.map((invoice) => ({
    id: invoice.invoice_id,
    number: invoice.invoice_number,
    issueDate: invoice.issue_date,
    dueDate: invoice.due_date,
    amount: invoice.amount,
    status: invoice.status,
  }))
}