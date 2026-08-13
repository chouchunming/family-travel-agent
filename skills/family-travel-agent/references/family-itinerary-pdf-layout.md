# Family Itinerary PDF Layout

Use this contract when creating or redesigning a family-facing itinerary PDF,
especially when it must remain readable on a phone. Preserve the trip plan as
the source of truth; layout work must not silently alter itinerary facts.

## Information architecture

1. Use portrait pages by default. Prefer A4 unless the user names another size.
2. Begin with a quiet cover, then a one-page reading guide and trip anchors.
3. Give each travel date its own execution page. Never place two normal days on
   one page merely to reduce page count.
4. Put secondary decision material after the daily pages: route menus,
   reservation or publication status, budget, and open loops.
5. Repeat field-critical information on the day where it is used even when it
   also appears in an appendix.

## Daily execution page

Use this visual hierarchy:

1. A high-contrast day banner with day number, date, weekday, and short theme.
2. A compact strip for lodging, party split, and the day's main objective.
3. A warning or hard-anchor card for fixed times and unresolved dependencies.
4. A vertical timeline or stacked itinerary rows with a suggested arrival and
   departure time for every stop, place, action, transport, duration, status,
   and a tappable Google Maps link. Avoid wide spreadsheet-style tables.
5. A three-meal block for breakfast, lunch, and dinner candidates.
6. A short reminder block containing only items needed to execute that day.

Every retained baseline and backup route must have its own executable timeline.
Do not give the baseline stop-by-stop times while leaving B/C alternatives as
one-line summaries. When the same backup can move across dates, deduplicate it
into a route menu and state its suitable dates, unsuitable dates, and activation
conditions instead of printing it once per day. Put that menu on adjacent
execution pages rather than shrinking the main day page.

For split-party days, show each party in clearly labeled cards. If one traveler
chooses among several reusable routes, keep the base day page concise and place
one deduplicated route menu in an appendix instead of repeating the same options
under every date. Expand each route into an executable stop-by-stop timeline
with suggested times and map links, and list the unsuitable dates with reasons
such as closure risk, fixed seasonal events, duplication, recovery needs, or a
family reunion deadline. A route sequence and prose description alone are not
sufficient.

## Time and map-link contract

- Give every baseline stop a useful time or time range. Include origin,
  transfers that require action, meals, lodging handoff, and the final return;
  omit only passive pass-through points.
- Label planning values as `建議`, historical timetable values as `舊季參考`,
  and evidence-backed fixed times as `已確認`. Never present an unpublished
  departure as a fixed time.
- Include realistic walking, parking, station, restroom, meal, luggage, child
  or elder, and winter-weather buffers. If a day still depends on an unknown
  timetable, show a planning skeleton and state which times must be rebuilt.
- Make the place name itself a tappable Google Maps URL. Prefer an official
  Maps place URL or a Maps search URL using the full unambiguous local-script
  place name and city.
- For driving, link to the verified visitor parking lot, vehicle entrance, or
  rental return entrance rather than a building center. If that target has not
  been verified, label the link `入口待確認` and do not invent coordinates or
  destination-specific navigation identifiers.
- Check that PDF link annotations exist and open as HTTPS URLs. Printed copies
  should still show enough place text to search manually; never display only a
  generic label such as `地圖`.

## Typography and density

- Use an embedded CJK font when the itinerary contains CJK text.
- Target at least 9 pt body text and 11 pt card headings; use 7.5 pt only for a
  compact appendix whose text remains legible after rendering.
- Keep line length short through stacked cards and two-column blocks. Do not use
  landscape orientation to rescue an over-wide table.
- Use 12–15 mm page margins and stable footer placement.
- Use one restrained palette: dark title color, one accent, one warning color,
  pale card backgrounds, and neutral rules. Color may reinforce but never be
  the only status signal.
- Prefer whitespace and page breaks over shrinking an entire page.

## Attraction field guide

Create one deduplicated field-guide entry for every actual attraction retained
in a baseline or backup route. Link or name that entry from the relevant day;
do not repeat the full description under every occurrence.

Use two levels of field-guide card so the document spends detail where it
changes execution:

- **Core attraction — complete card:** explain why it is worth the family's
  time, then give the actual walking/visit sequence, safe photo positions and
  shooting direction, quick/standard/deep dwell times, and family fit for
  stamina, outdoor exposure, wet-weather fallback, teen interest, and elder
  accessibility. Add seasonal or on-site difficulties, what to retain and cut
  when late, and evidence-dated reservation, opening, closure, and last-entry
  facts. End embedded photos with Chinese captions and a reminder that a
  representative view does not guarantee identical weather, foliage, snow,
  crowds, exhibits, or visibility on the visit date.
- **Backup attraction — compact card:** retain only why it is useful, visit
  order, standard dwell time, stamina/outdoor/weather fit, activation and
  cancellation conditions, and reservation state. Pack four to six compact
  cards per page in two columns when they remain readable. Promote a backup to
  a complete card if it becomes a fixed anchor or has meaningful safety,
  accessibility, or reservation complexity.

Write these as operational cards, not generic encyclopedia descriptions. If
the evidence cannot support a precise visit order, safe photo position, last
entry, or accessibility claim, label it for recheck instead of filling the
field with an assumption.

Each entry must contain:

- **Must-see / photo point:** the defining view, exhibit, street, room, or
  sequence worth prioritizing. Distinguish an official or well-established
  viewpoint from a planning recommendation, and never encourage entry into a
  closed, private, exposed, or traffic-conflicted area for a photograph.
- **Atmosphere:** a short sensory description that sets family expectations,
  such as quiet, crowded, contemplative, commercial, exposed, indoors, or
  weather-dependent. Include a realistic dwell pattern when useful.
- **Attention:** stamina, stairs, slope, walking distance, accessibility,
  footwear, weather exposure, child or elder fit, reservation, timed entry,
  last admission, closure, photography, food, or language constraints that can
  change whether the stop is suitable.

Attach a source and check date to changeable access, reservation, operating,
and restriction claims. If evidence is missing, say what must be checked rather
than inventing a highlight or rule.

### Attraction photo plates

When the user requests an illustrated itinerary, add a deduplicated photo plate
to each retained attraction entry. Prefer two representative real-world images
that help the family recognize the place: one defining overview and one detail,
seasonal view, or signature photo point. Use one image only when a second image
adds no execution value; use more only when the attraction has materially
different zones that the itinerary actually retains.

- Prefer official venue, tourism-board, government, or clearly licensed open
  media. Record the page URL, creator when supplied, license or reuse basis, and
  retrieval date. A public URL is not by itself permission to copy an image.
- Do not copy search-result thumbnails, hotlink unstable image URLs, remove
  watermarks, or present generated or stock imagery as documentary evidence.
  If reuse permission is unclear, provide a linked preview card or source-page
  link instead of embedding the image.
- Caption what the image shows and whether it is a current, seasonal, archival,
  or representative view. Do not imply that snow, foliage, illumination,
  crowds, visibility, exhibits, or food presentation will match the travel day.
- Crop without distorting or obscuring safety context. Keep attribution and
  source links legible in the PDF, and preserve enough resolution for phone
  viewing without inflating the file unnecessarily.
- Treat photo selection as navigation support, not decoration: align each image
  with the must-see/photo point, atmosphere, or an entrance/terrain caution.

Place attraction photo plates after the dated execution pages, adjacent to the
deduplicated attraction field guide. Do not place full attraction galleries on
daily pages when they would compete with times, maps, transport, or warnings.

Pack field-guide pages by measured content density rather than a fixed number
of attractions per page. Avoid leaving a half or more of a page blank merely
because the next entry belongs to a predetermined pair. Keep illustrated
entries together when practical; combine one illustrated entry with one or
more compact text-only entries when they fit. Arrange text-only entries in a
two-column grid or place several sequentially on one page. Let the document
engine flow a final entry to the next page when needed instead of inserting a
page break after every fixed-size batch.

Reduce whitespace before reducing type size. Tighten card spacing, captions,
and repeated guide instructions first, while keeping body text near 9 pt and
captions legible on a phone. Do not stretch photos, split a photo from its
attribution, orphan a heading, or compress safety and reservation cautions to
fill a page. During visual QA, flag guide pages with large avoidable blank areas
and repack them; intentional whitespace on a final short page is acceptable
only when the remaining entry cannot safely share the preceding page.

### Daily meal photos without pagination drift

When each normal date must remain exactly one page, use only the otherwise
unused lower portion of that date's execution page for recommended-dish photos.
Keep the timeline, three-meal text, warnings, and map links at their normal
minimum sizes. Add one or two compact dish images only when they fit without
moving any execution content to another page; otherwise reduce the image count
or omit images for that day. Never shrink the whole page, split one date across
pages, or let decorative images create a second page for the same date.

Caption each daily dish image with the exact restaurant or branch, recommended
dish, reservation state, and official promotional source. Use no generic or
unknown-source substitute when an official restaurant photo is unavailable.
The photo may illustrate a recommended dish but never turns an unverified menu
item or restaurant booking into confirmation.

## Status language

Display exact decision-relevant states in plain language: confirmed, candidate,
not published, site access blocked, dynamically unverified, unknown, and needs
verification. Do not expose sandbox policy, browser engines, automation tools,
HTTP retries, or internal debugging narration in a family-facing PDF.

Never turn a candidate, historical timetable, searchable listing, estimate, or
request into a confirmation. Put check dates beside time-sensitive prices and
schedules. Do not invent content to fill an empty card.

## Privacy and external-action boundary

Generate a family-facing copy without booking-management links, payment data,
or traveler identifiers unless the user explicitly requests a private execution
document. Rendering never authorizes booking, payment, email, form submission,
or disclosure of traveler data.

## Quality gates

Before replacing or handing off a PDF:

1. Validate page size, page count, metadata, and embedded fonts.
2. Extract text and assert every trip date and hard anchor is present.
3. Assert forbidden internal narration and disallowed private values are absent.
4. Render every page to images and inspect the cover, a normal day, the densest
   day, a split-party day, and each appendix type. Check all remaining pages for
   clipping, overflow, empty pages, tiny text, and broken glyphs.
5. Keep the prior PDF until the replacement passes these gates. Use a distinct
   output filename when the user may want to compare versions.
