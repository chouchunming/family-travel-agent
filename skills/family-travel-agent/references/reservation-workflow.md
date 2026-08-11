# Reservation Workflow

## States

Use exactly one state: `recommended`, `needs-booking`, `request-submitted`,
`confirmed`, `not-reservable`, `cancelled`, `replaced`, or `unknown`.

A request receipt is not confirmation. Use `confirmed` only when the provider
or official interface explicitly confirms the booking.

## Evidence extraction

Retain provider or venue, destination, date, time, party size, product or
course, useful original-currency price, mandatory fees, cancellation policy
and deadline, allergy or accessibility deadline, arrival/navigation
instructions, safe contact method, source, and check date. Keep personal data
and sensitive management links out of high-level summaries.

Compare new evidence with current state, explain the transition, preserve
conflicts, and update a reservation and its detailed day together when
authorized.

## Communication and action gate

Draft local-language or English email, phone dialogue, arrival phrases, and
concierge details. Research and drafting are read-only. Sending, submitting,
changing, cancelling, and paying require explicit approval for the exact
external action.
