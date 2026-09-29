# Provenance Ledger

Write one entry per reviewable change or experiment, when the work is done. Use exactly
the schema in HANDOUT.md. Put the prompts you typed into AI tools in `prompts/` and name
the file in the entry's `prompts` field.

## Worked example (not graded; leave it here and add your entries under "My entries")

This shows the level of detail expected. The commit SHAs, dates and numbers are made up.

```
## Entry 2
artifact:  askcode/split.py at commit 3f2a9c1
tool:      GitHub Copilot Chat in VS Code, model Claude Haiku 4.5, 2026-09-22
prompts:   asked for an ast loop that returns methods with class-qualified names;
           prompts/split-01.md
review:    read every line; rejected its use of ast.walk, which also returned nested
           functions and broke rule 1; rewrote the loop over tree.body and class bodies
           myself; kept its decorator handling after checking it against rule 3
checks:    pytest tests/test_split.py: 8 passed
evidence:  HANDOUT Step 2, split.py docstring rules 1 to 6
risk:      I did not test a file with Windows line endings

## Entry 5
artifact:  results/top3_words_five_part.csv at commit 8d41e07
tool:      askcode run_eval, anthropic claude-haiku-4-5-20251001, 2026-09-23
prompts:   the five-part prompt in askcode/prompt.py at commit 8d41e07;
           prompts/five-part-v1.md
review:    read all ten replies and marked the correct column against questions.json
checks:    python -m askcode.run_eval --search words --context top3 --prompt five_part:
           valid JSON 10 of 10, right place 6 of 10
evidence:  HANDOUT Step 5
risk:      one run only; a fresh run may answer differently
dataset:   questions/questions.json at commit 51c0e2a; corpus requests v2.32.3
result:    correct 6 of 10, 24,113 input tokens; results/top3_words_five_part.csv
changed:   two misses were retrieval failures, so I looked at why word search missed
           them before touching the prompt
```

## My entries

## Entry 1
artifact: .env.example and .env at commit c80990a
tool: provider openai, model gpt-5.6-luna. Input token cost per MTOKEN: 0.10, Output token cost per MTOKEN: 0.50
prompts: Google search for OpenAI pricing - https://developers.openai.com/api/docs/pricing
review: My model is luna, so I found that in the chart
checks: python -m askcode.check_setup
evidence: All checks passed
risk: Accidentally recording the wrong model

## Entry 2
artifact: search_words.py at commit f4737df
tool: Copilot, for splitting words properly
prompts: How to properly extract words? Split didn't work, I need to be able to handle _ and stuff
review: Solution is consistent with my regex knowledge. But it also didn't fix my problem of breaking up based on _ being a word boundary, so I had to remove _ from the regex.
checks: ai_replies/copilot_entry_2.txt (I didn't understand the ledger requirement at first, which is why I went back later to add the actual AI output)
evidence: All test cases related to search_words passed (test_search.py)
risk: If there is an edge case I didn't think about

## Entry 3
dataset:   results/*.csv at d84a4be
result:    results/summary_step_5.txt
changed:   I determined that the gold result was the best, which confirms that reading the whole corpus does not make it better (more is not always better).

## Entry 4
artifact: answer.py at commit f4737df
tool: Copilot, for processing data types properly
prompts: How to properly check if something is in int, because it appears it is classifying a true as an int
review: This is consistent with my understanding of datatypes. Also, it talked about floats, but I ommitted any references to floats in my code since I know line line must be an int.
checks: ai_replies/copilot_entry_4.txt
evidence: All test cases related to answer.py passed
risk: Low risk, this is a very simple question, mitigated by testing. It could mess up a few edge cases if wrong.

## Entry 5
dataset:   results/retrieval_meaning.csv at 1706a37
result:    results/summary_step_7.txt
changed:   retrieval_meaning got 9 out of 9 vs 5 out of 9 for retrieval_words
The ones it got right that the other got wrong:
Which function adds cookies to the cookiejar?
After a response is complete, what cleanup happens for the connection?
What adds the status codes list to the documentation?
How do hooks get registered?
