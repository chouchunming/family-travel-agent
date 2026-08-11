# Experience Planning Design

## Goal

Extend `japan-family-travel` with a reusable workflow for finding and comparing
family-suitable bookable experiences in Japan without treating any sales
channel as inherently authoritative or cheapest.

## Scope

The workflow covers experiences discovered through an operator's official
site, Agoda, KKday, and Klook. It does not automate purchases, submit booking
forms, store personal trip data, or add runtime dependencies.

## Structure

Add `references/experience-planning.md` and route experience, activity, tour,
workshop, ticket, and factory-visit requests to it from `SKILL.md`. Keep the
platform-specific rules out of the general itinerary reference so ordinary
planning does not load unnecessary detail.

## Discovery and evidence

- Search official operator pages and Agoda, KKday, or Klook as relevant; a
  recommendation does not require a listing on every channel.
- Use the operator's official source to verify that the experience exists and
  to check operating dates, eligibility, access, and core restrictions when
  that source is available.
- Use each live sales page for its own price, inclusions, inventory, payment,
  refund, cancellation, language support, transport, and platform-added
  benefits.
- When sources conflict, use the official operator for operating dates,
  eligibility, access, safety, and core restrictions, and use each seller for
  that seller's price, inventory, inclusions, payment, refund, and support
  contract. If an unresolved conflict affects date, eligibility, or safety,
  label it and do not present the candidate as ready to book.
- Record the check date for changing facts. Mark unavailable facts as
  `needs-verification`; never infer them.
- Treat user-provided confirmations as stronger booking evidence than a search
  result or product page.

## Family-fit and route checks

Compare date and time, total party price, included and excluded items,
age/height/health constraints, language, duration, meeting point, transport,
weather handling, cancellation deadline, and payment method. Fit candidates
around fixed reservations, meals, rest, transfers, hotel location, Japanese
holidays, weekends, and peak periods.

Compare total party prices after mandatory taxes and fees. Preserve each
seller's original currency. When a common-currency estimate materially helps,
label it as approximate and record the exchange-rate source and check date.

Recommend one to three candidates. Rank by family fit, route efficiency,
booking confidence, language accessibility, cancellation flexibility, and
value rather than discount alone. Include indoor or low-weather-risk
alternatives when weather can materially affect the day.

## Channel comparison output

For the same experience sold through multiple channels, show a compact
comparison containing:

- channel and direct link;
- date/time and availability status;
- original price and total party price including mandatory taxes and fees;
- approximate common-currency price, exchange-rate source, and check date when
  conversion materially helps;
- inclusions and material exclusions;
- language and family restrictions;
- cancellation/weather terms;
- booking-state confidence and check date;
- recommended booking channel with a short reason.

Do not claim the official channel is cheapest or best. Recommend whichever
channel best balances verified content, total cost, language, payment
convenience, cancellation flexibility, and support.

## Booking-state and action boundary

A searchable or purchasable listing is only a candidate. Payment or a request
receipt is not proof of confirmation. Reuse the reservation workflow's booking
states and require explicit approval before sending, submitting, cancelling,
or paying.

## Testing

Extend the packaged reference contract and repository file-shape/privacy tests
before adding the reference. Tests must require routing to the new reference
and preserve the following concepts: Agoda, KKday, Klook, official-source
cross-checking, family fit, route efficiency, language, cancellation, weather,
source-conflict handling, mandatory taxes and fees, exchange-rate source, check
date, `needs-verification`, one-to-three recommendations, booking-state
distinction, and explicit approval for external actions.

Run the repository suite, packaged contract, installed-link suite when the
canonical symlink is available, and the system skill validator through
`caffeinate -i -m`.

## Non-goals

- No scraping or platform API integration.
- No platform credentials or affiliate behavior.
- No live booking, payment, cancellation, or outbound messages.
- No real traveler names, booking references, email addresses, phone numbers,
  or private filesystem paths in the package.
- No changes to the skill's explicit-invocation policy.
