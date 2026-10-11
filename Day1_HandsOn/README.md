# Day 1 Lab: API Mechanics (about 4.5 hours)
 
**Milestone to pass:**
1. Without notes, explain when to use **streaming, caching and batch**.
2. Your script handles **3 error types** correctly (Lab 5).
 
## Setup (10 min)
 
```bash
python -m venv .venv && source .venv/bin/activate
pip install anthropic
export ANTHROPIC_API_KEY='sk-ant-...'      # env var only, never in code or git
export CLAUDE_MODEL='claude-sonnet-5-5'    # optional; check the models page for current IDs
```
 
## Run order
 
| # | Script | Time | What you prove |
|---|---|---|---|
| 1 | `lab1_basics.py` | 45 min | The API is stateless. You can read `stop_reason` and parse JSON defensively. |
| 2 | `lab2_streaming.py` | 40 min | Streaming improves time-to-first-token, not cost. Errors can appear mid-stream. |
| 3 | `lab3_caching.py` | 60 min | You can see a cache write, a hit and a miss in `usage`, and calculate the savings. |
| 4 | `lab4_batch.py submit`, then `collect` later | 40 min | You can submit at 50% price and match results by `custom_id`. |
| 5 | `lab5_errors.py` | 60 min | You catch 3 real error types and your retry logic passes 3 offline tests. |
| 6 | Closed-book test (below) | 30 min | You can explain the three features from memory. |
 
**Method for every lab:** predict the output before you run it. Write the prediction in `notes.md`. Every wrong prediction is a gap found cheaply.
 
## The three-way decision (build this table from memory, then check)
 
| | Streaming | Prompt caching | Batch |
|---|---|---|---|
| Problem it solves | Waiting for long output | Paying and waiting to resend the same big prefix | Paying full price for bulk work nobody waits on |
| Use when | A human watches the output, or the request is long enough to risk timeouts | The same large prefix repeats (system prompt, tools, documents) within the cache lifetime | Large volume, independent items, can wait up to 24h (usually under 1h) |
| Do not use when | No one is watching the output | The prefix is small or changes every call | A user is waiting, or step N needs step N-1's answer |
| Effect on cost | None | Writes cost 1.25x (5 min) or 2x (1 h); reads cost about 0.1x or less | 50% off |
| Effect on latency | Faster first token | Lower on cache hits | Slower: minutes to 24 hours |
| Effect on answer quality | None | None | None |
| Gotcha | An error can arrive after HTTP 200 | There is a model minimum length, and below it nothing is cached and no error is raised. Prefix order matters. | Results come back out of order, so match on `custom_id`. |
 
They combine: batch + caching stack, and streaming + caching is common in chat apps.
 
## Closed-book test (cover the table above)
 
Answer in one or two sentences each. Aim for 8 of 10.
 
1. A support chatbot resends a 20k-token policy document with every user message. Which feature, and why?
2. You must classify 200,000 archived tickets by Friday. Which feature, and what is the trade-off?
3. A user watches a 900-word report being generated and complains of a blank screen for 20 seconds. Fix?
4. Your cache usage shows `cache_creation_input_tokens: 0` and `cache_read_input_tokens: 0`. Name two likely causes.
5. After editing the first line of your system prompt, every request becomes a cache write again. Why?
6. Your app receives HTTP 400. Retry or not? What do you do?
7. Your app receives HTTP 529 and then 429. Retry or not? How?
8. Streaming returned HTTP 200 but the answer stops mid-sentence. What happened, and what should you do?
9. A batch finishes and results are in a different order than you sent them. Is that a bug?
10. Why does a nightly report not need streaming, and why does a chat UI not need batch?
 
## Answer key (check after you answer)
 
1. **Caching.** The prefix repeats, so reads are about 90% cheaper and faster. Put the static document first and add `cache_control`.
2. **Batch.** 50% cheaper, and it can run asynchronously. The trade-off is up to 24h latency. Anything not finished in 24h expires and is not billed.
3. **Streaming.** It improves time-to-first-token and perceived speed. Total generation time stays about the same.
4. The prompt is below the model's minimum cacheable length (this raises no error), or `cache_control` is missing or misplaced. Also possible: the cache expired between calls.
5. A cache hit requires an identical prefix up to the breakpoint. Changing early content invalidates everything after it.
6. **No retry.** It is `invalid_request_error`, which is your bug. Read the message, fix the request, and log the `request_id`.
7. **Yes, retry** with exponential backoff and jitter. Honour `retry-after` on a 429. A 429 from a spend cap has no `retry-after` and will not clear by retrying.
8. An error or dropped connection after the 200 header. Keep the partial text, then retry, resume, or show it. Don't assume success from the status code.
9. **No.** Batch results are not ordered, so match on `custom_id`.
10. Nobody watches a nightly report, so streaming adds nothing and batch can halve the cost. A chat UI cannot wait for batch latency.
 
## Scoring
 
- **8-10:** Day 1 passed. Move to Day 2.
- **5-7:** Redo the labs where you missed answers, then retake the test tomorrow morning before Day 2.
- **Under 5:** Do not move on. Repeat Labs 3 and 4 and re-run the test.
 
## Evidence to keep (portfolio for client conversations)
 
- `notes.md` with your predictions and what actually happened
- The Lab 3 output showing write, hit and miss, with your savings figure
- The Lab 5 "ALL PASS" output
- A one-page "Streaming vs caching vs batch" explainer in your own words that you could hand to a client
 
## Version note
 
Newer SDK versions raise a separate `OverloadedError` for 529. It is not a subclass of `InternalServerError`, so Lab 5 handles both. Run `pip show anthropic` to see which version you have.