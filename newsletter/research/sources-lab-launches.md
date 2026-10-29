# Weekly AI launch sweep: verified source list (as of 2026-10-29)

All URLs fetched on 2026-10-29 unless marked. "RSS: yes" means a 200 with XML from that feed URL.

## 1. First-party release pages and changelogs

| Source | URL | Good for | Cadence | RSS? |
|---|---|---|---|---|
| OpenAI News | https://openai.com/news/ | All launches (models, Codex, enterprise) | Multiple/week | **Yes**: https://openai.com/news/rss.xml (HTML page 403 to bots; feed works) |
| OpenAI API changelog | https://developers.openai.com/api/docs/changelog | Quiet API launches | Several/week | No (append `.md` for Markdown; /llms.txt) |
| OpenAI model release notes / ChatGPT release notes | https://help.openai.com/en/articles/9624314-model-release-notes and https://help.openai.com/en/articles/6825453-chatgpt-release-notes | ChatGPT-side rollouts | Weekly | No; **403 to bots**, needs headless browser |
| Anthropic News | https://www.anthropic.com/news | Models, enterprise, gov deals | Daily-ish | No (/news/rss.xml is 404) |
| Claude API release notes | https://platform.claude.com/docs/en/release-notes/overview | API/SDK/Console changes | Several/week | No |
| Claude apps release notes | https://support.claude.com/en/articles/12138966-release-notes | Consumer/Team features | ~2/month | No |
| Claude Code CHANGELOG | https://github.com/anthropics/claude-code/raw/refs/heads/main/CHANGELOG.md | Claude Code feature drops | Near-daily | GitHub commits feed |
| Google DeepMind blog | https://deepmind.google/blog/ | Frontier models | Weekly | **Yes**: https://deepmind.google/blog/rss.xml |
| Google Keyword AI | https://blog.google/technology/ai/ | Consumer/enterprise Gemini launches | Daily | **Yes**: https://blog.google/technology/ai/rss/ |
| Gemini API changelog | https://ai.google.dev/gemini-api/docs/changelog | Model GA dates | Weekly | No |
| Gemini app release notes | https://gemini.google/release-notes/ | App features | 2-3/month | No |
| Google Workspace Updates | https://workspaceupdates.googleblog.com/ | Gemini-in-Workspace | Daily | **Yes**: https://workspaceupdates.googleblog.com/atom.xml |
| Google Cloud AI blog | https://cloud.google.com/blog/products/ai-machine-learning | Gemini Enterprise, monthly roundup | Daily | No |
| Meta AI blog | https://ai.meta.com/blog/ | Low volume | Monthly | No |
| xAI News | https://x.ai/news | Grok models/APIs | ~2/month | No; **403 to bots** |
| Mistral News | https://mistral.ai/news | Models | Weekly | **Yes**: https://mistral.ai/rss.xml |
| DeepSeek API docs news/updates | https://api-docs.deepseek.com/news and https://api-docs.deepseek.com/updates | Model/API changes | Monthly | No |
| DeepSeek on HF | https://huggingface.co/deepseek-ai | Weights drop first here | Event-driven | HF API |
| Qwen on HF | https://huggingface.co/Qwen | Qwen weights (qwen.ai/blog is JS-only) | Weekly | HF API |
| Kimi / Moonshot | https://www.kimi.com/blog and https://huggingface.co/moonshotai | Kimi releases | Monthly | No |
| Zhipu / Z.ai | https://huggingface.co/zai-org | GLM family (z.ai/blog is 404) | Monthly | HF API |
| MiniMax | https://www.minimax.io/news and https://huggingface.co/MiniMaxAI | M-series | Monthly | No |
| Cohere blog | https://cohere.com/blog | Enterprise/finance | Weekly | No |
| AI21 blog | https://www.ai21.com/blog/ | Specialized post-training | Weekly | No |
| AWS ML blog / Nova | https://aws.amazon.com/blogs/machine-learning/ and https://aws.amazon.com/ai/generative-ai/nova/ | Nova, Bedrock AgentCore | Daily | **Yes**: https://aws.amazon.com/blogs/machine-learning/feed/ |
| Microsoft AI (MAI) | https://microsoft.ai/news/ | MAI models | Weekly | No |
| Microsoft 365 blog | https://www.microsoft.com/en-us/microsoft-365/blog/ | Copilot launches (incl. Copilot for Finance/Legal) | Weekly | No |
| GitHub changelog | https://github.blog/changelog/ | Copilot | Daily | **Yes**: https://github.blog/changelog/feed/ |
| NVIDIA dev blog + corporate blog | https://developer.nvidia.com/blog/ and https://blogs.nvidia.com/ | Nemotron, NIM | Daily | **Yes**: https://developer.nvidia.com/blog/feed/ and https://blogs.nvidia.com/feed/ |
| Hugging Face blog | https://huggingface.co/blog | Open-model ecosystem | Daily | **Yes**: https://huggingface.co/blog/feed.xml |

HF API for exact timestamps: `https://huggingface.co/api/models?author=Qwen&sort=lastModified&direction=-1&limit=20`

## 2. Leaderboards / eval trackers

| Source | URL | Good for | Cadence | RSS? |
|---|---|---|---|---|
| Artificial Analysis | https://artificialanalysis.ai/ and https://artificialanalysis.ai/changelog | Intelligence Index; same-day evals of new models | Daily | No |
| AA GDPval-AA | https://artificialanalysis.ai/evaluations/gdpval-aa | Professional-work eval | On launch | No |
| Vals AI | https://www.vals.ai/ ; https://www.vals.ai/benchmarks/legal_index ; https://www.vals.ai/benchmarks/finance_index ; https://www.vals.ai/blog | Legal Index, LegalBench, Finance Index, Finance Agent, CorpFin, Tax | Days after launch | No |
| Scale SEAL | https://labs.scale.com/leaderboard | Professional Reasoning: Finance and Legal; Remote Labor Index | On launch | No |
| Arena (ex-LMArena) | https://arena.ai/leaderboard | Human-pref ranking | Continuous | No; **403 to bots** |
| Epoch AI | https://epoch.ai/data/ai-models , https://epoch.ai/benchmarks | Model database, ECI | Weekly | No |
| Vellum | https://www.vellum.ai/llm-leaderboard | Cross-bench table; lags | Monthly | No |
| SWE-bench | https://www.swebench.com/ | JS-rendered | On submission | No |
| LiveBench | https://livebench.ai/ | JS-only; stale | Irregular | No |
| HF trending / papers | https://huggingface.co/models?sort=trending and https://huggingface.co/papers | Open-weight launches within hours | Hourly | HF API |

## 3. Aggregators and newsletters

| Source | URL | Good for | Cadence | RSS? |
|---|---|---|---|---|
| AI News (smol.ai, now Latent Space) | https://latent.space/news/ | Best single recall of launches | Weekdays | **Yes**: https://latent.space/feeds/news.xml |
| Simon Willison | https://simonwillison.net/ | Hands-on model notes, same day | Daily | **Yes**: https://simonwillison.net/atom/everything/ |
| Interconnects | https://www.interconnects.ai/ | Open models | Weekly | **Yes**: https://www.interconnects.ai/feed |
| Zvi "AI #N" | https://thezvi.substack.com/archive | Thursday mega-roundup | Weekly | **Yes**: https://thezvi.substack.com/feed |
| Import AI | https://importai.substack.com/archive | Research/policy | Weekly (Mon) | **Yes**: https://importai.substack.com/feed |
| The Neuron | https://www.theneuron.ai/ | Mainstream launches | Weekdays | **Yes**: https://www.theneuron.ai/feed |
| TLDR AI | https://tldr.tech/ai | Link roundup | Weekdays | No |
| Ben's Bites | https://www.bensbites.com/archive | Agent tooling | ~3/week | **Yes**: https://www.bensbites.com/feed |
| The Rundown | https://www.therundown.ai/ | Mainstream | Daily | No |
| Last Week in AI | https://lastweekin.ai/ | Weekly recap | Weekly | **Yes**: https://lastweekin.ai/feed |
| The Batch | https://www.deeplearning.ai/the-batch/ | Weekly digest | Weekly (Wed) | No |
| Stratechery | https://stratechery.com/ | Strategy analysis | 3-4/week | Paid feed |
| Platformer | https://www.platformer.news/ | Policy/industry | 4/week | **Yes**: https://www.platformer.news/rss/ |
| Big Technology | https://www.bigtechnology.com/ | Interviews/analysis | Weekly | **Yes**: https://www.bigtechnology.com/feed |

## 4. Enterprise adoption and funding

| Source | URL | Good for | Cadence | RSS? |
|---|---|---|---|---|
| The Information AI | https://www.theinformation.com/topics/artificial-intelligence and https://www.theinformation.com/features/ai-agenda | Scoops | Daily, paywalled | No |
| TechCrunch AI | https://techcrunch.com/category/artificial-intelligence/ | Funding, product news | Hourly | **Yes**: https://techcrunch.com/category/artificial-intelligence/feed/ |
| Crunchbase News AI | https://news.crunchbase.com/sections/ai/ | Funding rounds | Daily | Feed 403 |
| Reuters AI / Bloomberg AI | https://www.reuters.com/technology/artificial-intelligence/ , https://www.bloomberg.com/ai | Deals, regulation | Daily | Both block bots; use search |
| Ramp AI Index | https://ramp.com/data/ai-index | Adoption by vendor | Monthly (mid-month) | No |
| Menlo Ventures | https://menlovc.com/perspective/ | State of GenAI in Enterprise (~Nov/Dec) | Annual | No |
| a16z Enterprise | https://a16z.com/enterprise/ | Enterprise AI surveys | Monthly | No |

## 5. Social

| Source | URL | Good for | Cadence | RSS? |
|---|---|---|---|---|
| HN front page | https://news.ycombinator.com/ (search: https://hn.algolia.com/) | Launches hit top 5 within an hour | Continuous | **Yes**: https://hnrss.org/frontpage |
| r/LocalLLaMA | https://www.reddit.com/r/LocalLLaMA/top/?t=week | Open-weight drops | Continuous | Reddit blocks bots; needs API auth or search |
| r/singularity | https://www.reddit.com/r/singularity/ | Closed-model hype/leaks | Continuous | Same |
| X accounts | @OpenAI, @OpenAIDevs, @AnthropicAI, @claudeai, @GoogleDeepMind, @GeminiApp, @xai, @MistralAI, @deepseek_ai, @Alibaba_Qwen, @Kimi_Moonshot, @Zai_org, @MiniMax__AI, @ArtificialAnlys, @arena, @valsai, @scale_AI, @EpochAIResearch, @swyx, @simonw, @natolambert | Launch-day posts; eval results within 24h | Continuous | See sources-x-twitter.md |

## 6. Law/finance vertical pages

| Source | URL | Good for | Cadence | RSS? |
|---|---|---|---|---|
| Claude for Financial Services | https://claude.com/solutions/financial-services | Agent templates, data connectors, customer stories | Monthly | No |
| Claude customers (filter Legal / Financial services) | https://claude.com/customers | Customer stories | Weekly | No |
| OpenAI financial services | https://openai.com/solutions/industry/financial-services/ (403 to bots) and https://openai.com/academy/financial-services | ChatGPT for Financial Services | Monthly | No |
| Google Cloud Financial Services | https://cloud.google.com/blog/topics/financial-services | FS launches | Weekly | No |
| Microsoft Industry blog (FSI) | https://www.microsoft.com/en-us/industry/blog/ | Copilot for Finance | Weekly | No |
| Cohere blog | https://cohere.com/blog | Finance research assistants | Weekly | No |

## Recommended search queries (date filter: past week)

1. `"introducing" (model OR "open weights" OR "open-weight") site:openai.com OR site:anthropic.com OR site:deepmind.google OR site:x.ai OR site:mistral.ai`
2. `"now available" (Gemini OR Claude OR GPT OR Grok OR Kimi OR Qwen OR DeepSeek OR GLM OR MiniMax) API`
3. `huggingface.co (DeepSeek OR Qwen OR Kimi OR GLM OR MiniMax OR Nemotron) new model release`
4. `"Artificial Analysis" OR "Intelligence Index" new #1 OR "launches at"`
5. `(Vals OR "Legal Index" OR "Finance Index" OR LegalBench OR FinanceBench OR GDPval) new model results`
6. `(Codex OR "Claude Code" OR Copilot OR "Gemini Enterprise" OR Antigravity OR "computer use") launch OR "generally available"`
7. `(OpenAI OR Anthropic OR Google) ("financial services" OR legal OR "law firm") partnership OR launch`
8. `"enterprise" AI adoption (Ramp OR Menlo OR a16z OR survey) report`
9. `site:news.ycombinator.com (model OR open weight) points`
10. `(Harvey OR Hebbia OR Legora OR Rogo OR "Thomson Reuters" OR LexisNexis) AI launch`

## Pitfalls

- **Bot-blocked (403)**: openai.com HTML pages, help.openai.com, x.ai, arena.ai, reddit.com, reuters.com, bloomberg.com, crunchbase feed. Use the OpenAI RSS feed, Reddit's authenticated API, and web search for the rest.
- **No RSS**: anthropic.com/news, both Claude release-notes pages, OpenAI API changelog, Gemini API changelog, gemini.google release notes, Vals, Scale, Artificial Analysis, Epoch. Fetch HTML and diff against last week's snapshot.
- **JS-only rendering**: qwen.ai/blog, livebench.ai, swebench.com, z.ai. Use HF org pages / HF API instead.
- **URL drift**: docs.anthropic.com → platform.claude.com; anthropic.com/solutions → claude.com; lmarena.ai → arena.ai; scale.com/leaderboard → labs.scale.com; news.smol.ai → latent.space/news; platform.openai.com/docs/changelog → developers.openai.com/api/docs/changelog. Keep redirects enabled.
- **Staleness**: Vellum, LiveBench, Meta AI blog. Do not treat silence as "no launch".

## If you could only check 10

1. https://latent.space/feeds/news.xml
2. https://openai.com/news/rss.xml
3. https://www.anthropic.com/news + https://platform.claude.com/docs/en/release-notes/overview
4. https://deepmind.google/blog/rss.xml + https://ai.google.dev/gemini-api/docs/changelog
5. https://artificialanalysis.ai/changelog
6. https://www.vals.ai/
7. https://huggingface.co/models?sort=trending
8. https://hnrss.org/frontpage
9. https://thezvi.substack.com/feed
10. https://www.theinformation.com/features/ai-agenda (paywalled)
