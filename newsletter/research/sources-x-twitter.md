# Pulling weekly posts from X/Twitter: state of play (2026-10-29)

Checked by live HTTP probes from the cloud sandbox plus vendor docs.

## Summary

| Route | Status | Cost | Verdict |
|---|---|---|---|
| Official X API v2 (pay-per-use) | Live; Free/Basic/Pro tiers gone | $0.005/post read; List endpoint works; ~$30-65/mo for 100 accounts | ToS-clean, reliable; the right choice if budget allows |
| twitterapi.io | Live | $0.15 per 1k tweets; list, user timeline, search | Cheapest working route (~$3/mo); runs on scraped account pools upstream |
| SocialData.tools | Live | $0.20 per 1k tweets | Same shape; fallback provider |
| Apify tweet-scraper | Live | $0.40/1k + paid Apify plan | Worse deal |
| Nitter / xcancel | **Dead** (C&D Aug 2026, xcancel suspended Sep 2026, repo archived Oct 2026) | — | Not viable |
| syndication.twitter.com / fxtwitter / vxtwitter / oEmbed | Single-post hydration only; timeline endpoints rate-limit datacenter IPs (429) | Free | Only to expand a known post URL |
| Cookie-based scrapers (twscrape, twikit) | twscrape maintained; needs burner account pool | Free + proxy | ToS breach, ban risk; avoid |
| Bluesky public API + X mirror bots | **Verified working, unauthenticated** | Free | Backbone of the zero-cost fallback |
| Grok `x_search` tool | Live; citations return x.com post URLs | $5 per 1k posts fetched + tokens; 20-handle limit | Good for topical "what did people say" sweeps, not a timeline reader |

## Verified free route: Bluesky mirrors

`https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=<handle>&limit=50` works with no key. Verified 2026-10-29 with posts from 2026-10-28:

- `anthropicai.xmirror.bot` (mirror of @AnthropicAI)
- `openai.xmirror.bot` (mirror of @OpenAI)
- `googledeepmind.zpravobot.news.ap.brid.gy` (Mastodon mirror of @GoogleDeepMind bridged to Bluesky)
- Native accounts that post directly: `simonwillison.net`, `emollick.bsky.social`

Keyword search (`app.bsky.feed.searchPosts`) needs a free account + app password. Mirror bots are unofficial and may disappear under the same legal pressure that killed Nitter; treat them as a bonus.

Recall estimate vs. X: lab accounts ~90% via mirrors while they last; named researchers 30-50%; legal-tech and fintech commentators lower.

## Official X API details

- Pricing: https://docs.x.com/x-api/getting-started/pricing. Post read $0.005 per post returned, applies to user timelines, recent search, and `GET /2/lists/:id/tweets`. Prepaid credits with a spend cap.
- Recent search: 7-day window, 450 req/15 min.

```
GET https://api.x.com/2/lists/{LIST_ID}/tweets?max_results=100&since_id=...&tweet.fields=created_at,entities&expansions=author_id
Authorization: Bearer $X_BEARER
```

## twitterapi.io details

- Pricing: https://docs.twitterapi.io/pricing (15 credits/tweet; 100k credits = $1; free trial credit).
- Endpoints: `GET /twitter/user/last_tweets?userName=OpenAI`, `GET /twitter/list/tweets?listId=...`, `GET /twitter/tweet/advanced_search?query=...`.

## Grok x_search

- Docs: https://docs.x.ai/developers/tools/x-search ; pricing https://docs.x.ai/developers/pricing.
- `allowed_x_handles` (max 20), `from_date`/`to_date`; citations in `response.citations`.

## Recommended stacks

**$0-30/month:** twitterapi.io reading one private X List plus 3-5 `advanced_search` queries (expected < $3/mo). Fallback 1: SocialData.tools. Fallback 2 (free): Bluesky `getAuthorFeed` over a handle map (official, `*.xmirror.bot`, `*.brid.gy`) plus lab RSS.

**$100-200/month:** official X API pay-per-use on the List endpoint (~$30-70/mo, ToS-clean) with a console spend cap; add Grok x_search for topical sweeps (~$20-40/mo); keep twitterapi.io as fallback.

**Mechanics:** `handles.yaml` as source of truth (handle, X user_id, bluesky_handle, rss_url, tags). One private X List owned by a dedicated low-value account. Read the List timeline with `since_id` persisted between runs; dedupe on post id; expand retweets/quotes to the referenced post; fall back to per-handle reads for handles missing from the List.

## Risks to disclose

- Resellers run on scraped account pools; X's ToS forbids this and X litigates (Nitter). Design for provider swap.
- Cookie scrapers and Nitter self-hosting put the account at ban risk; burner-only, and still a ToS breach.
- Official API pricing has changed four times in 18 months; cap spend.
- Mirror bots are unofficial; backbone should not depend on them.
- Undocumented endpoints (syndication, fxtwitter) already rate-limit datacenter IPs.
