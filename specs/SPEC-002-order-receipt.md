# SPEC-002 — Downloadable order receipt

**Status:** ready for implementation
**Owner:** Product, Patient Experience

## Why

Patients claiming on private health insurance need a receipt showing the medication, the
price and the date. Today they screenshot the order page, and insurers reject it. This is
the second most common support request after delivery tracking.

## What

A signed-in patient can download a receipt for any completed order.

1. A **Download receipt** action on the order detail page produces a PDF.
2. The receipt shows: order reference, order date, patient name and delivery address,
   line items with quantity and price, VAT where applicable, and the total paid.
3. Pharmacy staff can export a month of orders as a CSV file for reconciliation.
4. The downloaded file is named after the order reference and the date.

## Acceptance criteria

- [ ] A patient can download receipts only for their own completed orders.
- [ ] An order that is not yet completed offers no receipt.
- [ ] The PDF opens correctly in the common desktop and mobile viewers.
- [ ] The CSV opens in Excel without a warning and without any cell being interpreted as
      a formula.
- [ ] Generating a receipt does not change the order.
- [ ] Receipt generation for a large month-end export does not block the application.

## Notes for implementation

- We have no PDF library in the project yet, so one has to be introduced. Choose a
  maintained library with a licence compatible with commercial distribution, and check it
  against policy **before** adding it to `pom.xml`.
- The CSV export takes a start and end date supplied by the user.
- Receipts are generated on demand and are not stored.

## Out of scope

Emailing receipts, insurer-specific templates, historical orders older than seven years.
