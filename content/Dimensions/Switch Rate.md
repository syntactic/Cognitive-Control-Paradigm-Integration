#dimension

Definition: A parameter governing the between-trial task sequence structure. It refers to the probability that the task required on the current trial (N) will be different from the task required on the previous trial (N-1).

**Values:** **Continuous (%)**, typically ranging from 0% to 100%.

- Switch Rate = 0%: Pure task blocks (no task switching).
- Switch Rate = 50%: Random task switching (for two tasks).
- Switch Rate = 100%: Predictable task alternation (e.g., ABAB).
- Can also describe predictable sequences (e.g., AABB, implying specific switch probabilities at certain points).

**Relevance to Design Space:**

- A defining dimension of [[Task Switching]] paradigms.
- Switch Rate = 0% characterizes [[Single Task]] and (most) [[Dual-Task Performance & PRP|PRP]]/[[Dual-Task Performance & PRP|Dual Task]] blocks.
- Manipulating switch rate investigates how participants adapt preparatory strategies based on task predictability.
- In **Number of Tasks=2** paradigms, a non-zero switch rate (typically 50%) is used to represent **trial-to-trial uncertainty in task presentation order**. Instead of switching the task rule set itself, it models the randomization of which task appears as S1 and which as S2. This makes it a key parameter for representing "bridge" paradigms like [[Sigman & Dehaene (2006)]] that mix dual-task execution with scheduling uncertainty.

Super Exp. Mapping (Client-side - experiment.js): Implemented by the logic in createTrialSequence, which determines the task_1 (and potentially task_2) parameter for each trial based on the desired switch probability or sequence.