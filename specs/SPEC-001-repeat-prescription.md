# SPEC-001 — Repeat prescription ordering

**Status:** ready for implementation
**Owner:** Product, Patient Experience

## Why

Most of our prescription volume is repeat medication. Today a patient has to search the
catalogue again and rebuild the basket every time, which is the single most common reason
people abandon an order. Support handles roughly 400 calls a month that begin with
"I just want the same thing as last time".

## What

A signed-in patient can reorder a previous prescription in one step.

1. On the order history page, every previous order that contained a prescription item
   shows a **Reorder** action.
2. Selecting it opens a confirmation page listing the medication, quantity and the
   prescribing practice from the original order.
3. The patient may attach an updated prescription document if the original has expired.
   Accepted formats: PDF, JPEG, PNG. Maximum 10 MB.
4. On confirmation, a new order is created with the same items and the patient's current
   delivery address, and the order reference is shown.

## Acceptance criteria

- [ ] A patient sees Reorder only on their own orders.
- [ ] Requesting a reorder for an order that belongs to somebody else is refused, and the
      refusal does not reveal whether that order exists.
- [ ] An expired prescription cannot be reordered without a new document attached.
- [ ] Uploaded documents are retrievable only by the patient who uploaded them and by
      pharmacy staff.
- [ ] The original order is never modified.
- [ ] Reorder of a medication that is no longer available shows a clear message and does
      not create an empty order.

## Notes for implementation

- Order lookup happens by order reference, which is supplied by the client.
- The uploaded document keeps its original file name for the pharmacist's benefit.
- Search across order history should support partial matching on medication name.
- Every reorder is written to the audit log, including who triggered it.

## Out of scope

Payment changes, subscription or scheduled repeat delivery, prescriber verification
against the NHS Electronic Prescription Service.
