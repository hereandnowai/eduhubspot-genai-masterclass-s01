# Prompt Engineering: Unlock Your LLM's Full Potential

**Date:** 2026-04-12
**Created by: Ruthran Raghavan, Chief AI Scientist, HERE AND NOW AI**

---

## 1. Hook & Intro

**Side-by-side: Bad prompt vs. great prompt**

* **Bad prompt:**

  > Write something about our product.
  >

  * **Result:** Generic marketing fluff, wrong tone, wrong length, no clear CTA.
* **Great prompt:**

  > You are a senior B2B copywriter. Write a 2-sentence LinkedIn ad for our project-management SaaS (Asana alternative). Audience: ops managers at mid-size companies. Tone: confident but not salesy. End with a clear CTA to start a free trial. No emojis.
  >

  * **Result:** On-brand, scoped, actionable, and easy to drop into an ad.

> "Most people are leaving 80% of an LLM's capability on the table."

---

## 2. What Is Prompt Engineering & Why It Matters

**Programming in natural language**

* You’re giving instructions in plain language instead of code.
* The model has no built-in “task list”—you define the task, role, format, and constraints in the prompt.
* The same model can seem brilliant or useless depending on clarity, context, and structure.

**Example:**

* **Vague:** “Help with my essay.” → Model doesn’t know subject, length, or style.
* **Specific:** “You are a tutor. Help me improve the thesis and first paragraph of this 500-word history essay on the causes of WWI. Keep my voice; suggest edits inline.” → Model can actually help.

**Who benefits:**

* **Developers:** code generation, debugging, docs, refactors.
* **Marketers:** copy, ads, emails, social, A/B ideas.
* **Researchers:** summarization, lit review, brainstorming.
* **Everyday users:** writing, planning, learning, decision-making.

---

## 3. Foundation: How LLMs "Think"

**Next-token prediction (intuition only)**

* The model predicts the next token (word or sub-word) given everything so far in the prompt and conversation.
* It has no memory of past chats unless you include that information in the current context.
* **So:** context, specificity, and structure in your prompt directly shape what it says next.

**Steering vs. commanding**

* **Commanding:** “Summarize this.” → Model chooses length, style, and focus.
* **Steering:** “You are an executive assistant. Summarize this meeting transcript in 4 bullet points. Focus on decisions and action items. No filler.” → You steer length, focus, and format.

---

## 4. Core Techniques

### 4a. Be Specific & Set the Scene

Define role, audience, tone, and format.

* **Role:** “You are a senior technical writer.”
* **Audience:** “Writing for developers who know Python but not cloud APIs.”
* **Tone:** “Professional but friendly; avoid jargon or explain it once.”
* **Format:** “Start with a 2-sentence overview, then numbered steps, then a short ‘Common pitfalls’ section.”

### 4b. Few-Shot Prompting

Give 2–4 examples of input → output pairs. The model infers the pattern and replicates it.

* **Example:** Turn feedback into ticket titles using the format `[Area] Brief description`.
  * *Input:* "Login is broken with Google on Safari." -> *Output:* `[Auth] Google login fails on Safari`
  * *Input:* "The app crashes when I upload a PDF over 10MB." -> *Output:* `[Upload] Crash on large PDF`

### 4c. Chain-of-Thought (CoT)

Ask the model to **think step by step** before giving the final answer. This reduces logic and math errors.

* *Prompt snippet:* "Think step by step: find subtotal, then apply discount, then state final amount."

### 4d. Structured Output

Ask explicitly for **JSON, Tables, XML, or Markdown** so you can parse and use the output.

* *Prompt snippet:* "Respond with valid JSON only, no other text, in this shape: `{ "products": [...] }`"

### 4e. Constraints & Negative Instructions

Say what you **don’t** want (length, tone, format, or topic).

* **Length:** "Exactly 3 bullet points."
* **Tone:** "No slang or humor."
* **Scope:** "Do not suggest paid tools."

### 4f. Iterative Refinement

Treat prompting as a conversation.

* 1. Draft -> 2. "Shorter" -> 3. "More formal" -> 4. "Add Google Calendar mention".

### 4g. Interview-style Prompting

Let the model ask **you** questions first.

* *Prompt snippet:* "Before you do this, interview me: ask me any questions you need answered to do this well. Ask one at a time."

---

## 5. Advanced Strategies

* **System vs. User Prompts:** Use System prompts for "always-on" rules (identity, safety) and User prompts for the specific task.
* **Prompt Chaining:** Break complex tasks into steps. Use output of Step 1 as input for Step 2.
* **Self-Evaluation:** Ask the model: "Rate this summary 1–5 for clarity. Suggest one improvement."
* **Temperature:** Low (0.2) for facts/code; High (0.8) for brainstorming.

---

## 6. Common Mistakes & How to Fix Them

| Mistake                   | What goes wrong           | Fix                                 |
| :------------------------ | :------------------------ | :---------------------------------- |
| **Too vague**       | Generic/irrelevant output | Add role, audience, tone, format    |
| **Too many tasks**  | Model drops tasks         | Split into steps (chaining)         |
| **No context**      | Wrong style               | Add background or few-shot examples |
| **Ignoring format** | Hard to reuse             | Request JSON/Tables                 |
| **Assuming memory** | Model "forgets"           | Summarize key facts in current turn |

---

## 7. Real-World Use Case Walkthroughs

* **Writing:** Blogs, emails, ad copy.
* **Code:** Debugging, refactoring, adding tests.
* **Data:** Summarization, trend analysis in tables.
* **Research:** Brainstorming names or pros/cons.

---

## 8. Toolkit & Resources

* **Libraries:** PromptBase, FlowGPT, OpenAI/Anthropic examples.
* **Journaling:** Save prompts that work! Note what you changed when they failed.

---

## Wrap-up

Prompt engineering is **programming in natural language**. Small changes in how you ask can unlock 80% more value from the model.

**Next step:** Pick one technique (like "Be Specific" or "Few-Shot") and apply it to a task you do every week. Save the result!
