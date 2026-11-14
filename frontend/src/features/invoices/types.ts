export type Invoice = {
  id: string
  number: string,
  issueDate: string,
  dueDate: string,
  amount: string,
  status: 'open' | 'paid' | 'overdue' | 'cancelled'
}