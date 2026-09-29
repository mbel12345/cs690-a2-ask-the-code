# Assignment 2 Report: Ask the Code

Name: Matthew Belanger
Provider and model: OpenAI gpt-6-luna
Prices used (per million tokens, input and output), and the page you found them on:
input = 0.10
output = 0.50
https://developers.openai.com/api/docs/pricing

## Table 1. Finding the right function

| Run | Right function in top 3 |
| --- | --- |
| retrieval_words | 5 of 9 |
| retrieval_meaning | 9 of 9 |

## Table 2. Answers

| Run | Valid JSON | Right place | Correct (your marks) | Input tokens | Output tokens | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- |
| top3_words_five_part | 10 of 10 | 5 of 10 | 7 of 10 | 13,013 | 470 | 0.0015 |
| whole_five_part | 10 of 10 | 7 of 10 | 9 of 10 | 546,743 | 403 | 0.0549 |
| gold_five_part | 10 of 10 | 10 of 10 | 10 of 10 | 3,598 | 530 | 0.0006 |
| top3_words_minimal | 4 of 10 | 2 of 10 | 7 of 10 | 11,456 | 2,729 | 0.0025 |

## 1. Whose fault is it? (Step 5)

One row for every question marked `no` in top3_words_five_part. Take the first three
columns from Table 3 of `python -m askcode.summary`. Fault is retrieval, generation or
both, following the rule in Step 5. Evidence is one sentence about what you saw in the
reply or the retrieved functions.

| Question | Hit in top 3 | Correct with gold context |
| --- | --- | --- |
| q05 | no | yes | retrieval; this was a conceptual question about cleaning up connections, so it makes sense that word-match alone wouldn't work.
| q06 | no | yes | retrieval; the relevant function pulls data into the help menu, and this relationship would be hard to explain based on words alone
| q08 | no | yes | retrieval; this is an open-ended question, so hard to answer just based on looking for the same words

## 2. Paste everything or search? (Step 5)

Compare top3_words_five_part with whole_five_part: correct answers, input tokens and cost
for each, from Table 2. In two or three sentences: did pasting the whole codebase give
better answers, and was the difference worth the price?

Whole got 7 correct vs. 5 for top3.
Input tokens for whole where 546,743; input tokens for top3 where 13,013.
Cost for whole 0.0549, top3 was 0.0015.
Doing the whole code base did give correct answers, 40% more correctness. But the price was 37 times as much. So I don't think it is worth the price increase.


## 3. Minimal prompt against five-part prompt (Step 6)

Which prompt did better on right place, and which on correct? Give both numbers for both
prompts. Name one question where the two prompts' replies differed, and say what
differed.

Whole five part had 9 right and gold five part had 10 right. Minimal had only 7 right.
Whole five part had 7 right place and gold five part had 10 right place. Minimal had only 2 right place.
What adds the status codes list to the documentation? Minimal says there is no code that adds them to the doc, whereas the five-parts correctly mention the _init() function.


## 4. Word search against meaning search (Step 7)

Name one question meaning search ranked higher than word search, and one question word
search ranked higher than meaning search, with the ranks from Table 4 of
`python -m askcode.summary`. If no such question exists, say so. In one sentence each,
say why you think each search won.

meaning did better at question 4 (Can you pass JSON to a delete request?), probably because it required an understanding of how kwargs worked (at first glance, this doesn't look like you can pass it).

word search did not do better in any cases, this is probably because meaning is largely dependent on words so any patterns picked up by word search are probably factored into meaning.
## 5. Your decision rule (Step 8)

One rule for this codebase: when would you paste everything, and when would you search?
Cite the measured cost and the measured correct count of both designs.

I would paste everything when the question is asking how different functions interact with each other. I would search for things like info about specific functions or self-contained logic. Whole cost was 0.0549 vs. 0.0006 for gold.
Gold is also more accurate, with 10 out of 10 for both right place and right answer, vs. 7 right place and 9 right answer for whole.
