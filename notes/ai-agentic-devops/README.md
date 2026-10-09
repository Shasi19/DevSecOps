# AI and agentic AI for DevOps

## Mental model

An AI assistant generates predictions from input context; an agent adds a loop that selects tools, observes results, and may act repeatedly. Neither is inherently correct or safe. Treat model output, retrieved documents, tool results, and user-supplied text as untrusted inputs, and constrain what actions an agent can take.

## Useful applications

Good early uses include log summarization, runbook discovery, configuration explanation, test generation, and incident-context synthesis. Keep deterministic systems responsible for authorization, policy enforcement, deployment gates, and safety-critical decisions. Measure whether AI improves task completion time and accuracy—not only response quality.

## Safe operating pattern

1. Define the task, permitted data, allowed tools, and stop conditions.
2. Retrieve only relevant, authorized context and minimize sensitive data.
3. Give tools narrow, scoped credentials; separate read-only diagnosis from mutation.
4. Validate structured outputs and independently verify commands/plans.
5. Require human approval for high-impact actions; record inputs, tool calls, and outcomes.

Defend against prompt injection in logs, tickets, source comments, and retrieved documents. Do not let instructions embedded in data override system policy. Add budgets, timeouts, rate limits, and loop limits. Avoid sending secrets or regulated data to a model provider unless policy explicitly permits it. Evaluate for hallucination, data leakage, unsafe tool use, and failure under adversarial or ambiguous input.

## Practice

Prototype a read-only incident assistant that summarizes alerts and links runbooks. Test it with hostile instructions inside sample log lines. Then add a separate, approval-gated action tool and prove it cannot execute arbitrary shell commands.

## Further reading

[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) · [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
