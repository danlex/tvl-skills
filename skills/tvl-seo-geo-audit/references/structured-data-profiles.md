# Structured Data Profiles

Use this reference after the general structured-data check identifies a page type. Validate that structured data is eligible, visible-content-consistent, and appropriate for the page.

Verified as of: 2026-08-16

## Common Profiles

| Page type | Useful schema | Required caution |
| --- | --- | --- |
| Article, blog, news, guide | `Article`, `BlogPosting`, `NewsArticle`, `BreadcrumbList`, `Person`, `Organization` | Do not fabricate author, date, publisher, or reviewed-by fields. |
| Product or ecommerce | `Product`, `Offer`, `AggregateRating`, `Review`, `MerchantReturnPolicy`, `OfferShippingDetails` | Price, availability, reviews, ratings, shipping, and returns must match visible content or trusted feeds. |
| Local business | `LocalBusiness`, subtype, `PostalAddress`, `OpeningHoursSpecification`, `GeoCoordinates` | NAP, opening hours, service area, and reviews must be visible and accurate. |
| Course or training | `Course`, `CourseInstance`, `Organization`, `FAQPage` when visible | Do not use Course schema for generic service pages. |
| Video page | `VideoObject`, `Clip`, `BroadcastEvent` when applicable | Video must be publicly accessible; thumbnails, duration, upload date, and transcript/captions should be verifiable. |
| FAQ or how-to support | `FAQPage`, `HowTo` where eligible and visible | Mark up only visible Q&A/steps and follow current rich-result eligibility. |
| Organization or person | `Organization`, `Person`, `sameAs`, `ContactPoint` | Avoid fake credentials, unsupported affiliations, and misleading social links. |

## Evidence Needed

- Parsed JSON-LD or microdata.
- Visible content matching each load-bearing property.
- Rich Results Test or equivalent validation when available.
- Page type and intent.

## Report Rules

- Missing optional schema is not a blocker by itself.
- Deceptive schema is a `STRUCTURED_DATA_BLOCKER`.
- Profile mismatch is at least `REVISE`; it becomes `BLOCK` when it misleads users or search systems.
