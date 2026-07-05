# Project Phases

## Phase 0: Foundation

Goal:
Create the project operating system and LangChain-first architecture before writing application code.

Deliverables:

- `README.md`
- `architecture.md`
- `working-standard.md`
- `specs.md`
- `task.md`
- `logs.md`
- `ASSISTANTS.md`
- `.gitignore`
- `private/` local note area
- default stack
- AI Reliability domain slice
- manual and automated testing standard

Scope:

- Document project intent, architecture, and development rules.
- Define the default stack and AI Reliability research slice.
- Establish private-material git exclusion rules.
- Set the LangChain-first plus LangGraph-early project approach.
- Capture manual and automated testing standards early.
- Keep project docs as the source of truth for phase planning.
- Record the Phase 0 Software Design Document in `specs.md`.

Exit conditions:

- Root project operating docs exist and agree on project direction.
- The architecture, stack, and private/public boundaries are documented.
- The phase roadmap and development rules are written and usable for future sessions.

Validation:

- Manual: read-through of root docs for consistency and missing decisions.
- Automated: `.gitignore` behavior checked for private paths and local-only material.

## Phase 1: LangChain OpenAlex Ingestion

Goal:
Use LangChain-compatible document abstractions while ingesting AI Reliability works from OpenAlex.

Operational sequencing for this phase:

- Start with Dockerized local development for PostgreSQL and the application runtime.
- Add the first CI checkpoint after one-work ingestion, Alembic migrations, and the first ingestion-focused tests are stable enough to enforce in pull requests.
- Close the phase only after manual PostgreSQL validation confirms ingestion, re-ingestion, and audit/error behavior.
- Run an architecture check before exit to confirm ORM, Alembic, SQL reference, ingestion services, API routes, and tests still agree on ownership.

Core tasks:

- Design and migrate the Phase 1 PostgreSQL schema.
- Implement ORM models, validation schemas, and database session management.
- Implement one-work ingestion with explicit upsert behavior.
- Add ingestion audit/error tracking, retry classification, and initial retry execution.
- Add Dockerized local PostgreSQL, manual runbooks, and first PostgreSQL-backed tests.

Exit conditions:

- All migrations apply cleanly to a real PostgreSQL instance.
- One real OpenAlex work can be ingested and re-ingested without duplicate entity rows.
- `ingestion_runs` and `ingestion_errors` capture expected audit behavior.
- PostgreSQL-backed ingestion tests pass.
- Manual validation confirms the stored rows match the intended schema and relationships.
- Architecture review confirms no duplicated ingestion business rules across routes, scripts, and services.

Validation:

- Manual: follow `src/ingestion/manual_test.md` end to end.
- Automated: run Alembic migrations plus the ingestion pytest suite against PostgreSQL.
- CI/CD maturity: first GitHub Actions workflow for lint, compile/import checks, PostgreSQL service, Alembic upgrade, and ingestion tests.

## Phase 2: LangChain Retrieval Core

Goal:
Implement searchable, filterable, citation-aware, and semantic scholarly retrieval with LangChain and `pgvector`.

Production API baseline already started:

- FastAPI has a real application entrypoint.
- Health, readiness, version, and Prometheus metrics endpoints exist.
- Request IDs, structured logging, normalized API errors, and pagination bounds exist.
- Retrieval responses already separate question, evidence, citations, and grounding status.

Core tasks:

- Define LangChain document mapping for ingested works and approved local material.
- Add embedding storage and retrieval-oriented metadata.
- Implement keyword, metadata-filtered, and semantic retrieval.
- Establish retrieval response contracts for evidence and citations.
- Keep retrieval ranking, evidence construction, and citation formatting owned by retrieval services.

Exit conditions:

- Ingested works can be converted into LangChain-compatible documents with consistent metadata.
- Retrieval supports basic search, metadata filtering, and cited evidence output.
- `pgvector`-backed semantic retrieval works on representative data.
- Retrieval behavior is stable enough to support the first workflow layer.
- API routes, AI services, and evaluation harnesses consume retrieval contracts instead of duplicating retrieval queries.

Validation:

- Manual: run representative scholarly queries and inspect returned evidence/citations.
- Automated: retrieval tests for filters, ranking expectations, and vector storage contracts.
- CI/CD maturity: add retrieval tests and pgvector/schema checks to the existing CI workflow once semantic retrieval lands.

## Phase 3: LangGraph Research Workflow

Goal:
Add the first stateful research workflow: question, retrieval, citation inspection, synthesis, grounding validation, and cited response.

Core tasks:

- Define workflow state, node transitions, and failure states.
- Implement evidence retrieval, citation inspection, synthesis, and grounding checks.
- Produce a cited response contract suitable for future UI/API use.
- Keep workflow orchestration separate from retrieval ranking and provider-specific inference calls.

Exit conditions:

- A research question can move through the complete workflow state machine.
- The workflow produces grounded, cited output using retrieval results.
- Failures and partial states are observable and recoverable enough for iterative use.
- LangGraph state owns orchestration while retrieval, inference, and evaluation remain separate modules.

Validation:

- Manual: execute representative research questions and inspect workflow traces.
- Automated: LangGraph state transition tests and regression cases for grounded output.
- CI/CD maturity: add deterministic workflow tests with mocked model calls; paid Azure OpenAI calls remain excluded from default CI.

## Phase 4: Evaluation

Goal:
Measure retrieval quality and answer grounding with repeatable tests.

Default implementation choice:

- Start with a local evaluation harness.
- Do not require paid Azure OpenAI calls in default CI.
- Add managed evaluation tooling only after local datasets, metrics, and thresholds are understood.

Core tasks:

- Define evaluation datasets and scoring criteria.
- Implement retrieval and grounding evaluation runs.
- Track regressions across changes to retrieval and workflow behavior.
- Keep evaluation scoring separate from retrieval and workflow implementation logic.

Exit conditions:

- Evaluation scenarios exist for retrieval, grounding, hallucination resistance, and privacy boundaries.
- Evaluation runs can be repeated and compared across revisions.
- The project has a usable baseline for future quality gates.
- Evaluation code consumes public service/workflow contracts and does not depend on private implementation details.

Validation:

- Manual: inspect evaluation reports for representative scenarios.
- Automated: repeatable evaluation scripts or tests that surface regressions.
- CI/CD maturity: add cheap local evaluation smoke checks and regression thresholds once the metrics are stable.

## Phase 5: Observability

Goal:
Track API requests, ingestion runs, retrieval traces, LangChain calls, LangGraph transitions, failures, latency, and eval history.

Default implementation choice:

- Prometheus and Grafana are the first observability stack.
- OpenTelemetry comes after core metrics are stable.
- LangSmith remains optional for LangChain-specific trace inspection.

Core tasks:

- Standardize structured logs and request/run identifiers.
- Capture ingestion, retrieval, and workflow execution traces.
- Record failure, latency, and evaluation history for debugging and review.
- Centralize metrics and logging conventions so each service does not invent its own observability shape.

Exit conditions:

- Major platform actions emit traceable observability records.
- A developer can reconstruct what happened during ingestion, retrieval, and workflow execution from stored records.
- Observability remains a cross-cutting layer rather than business logic embedded in domain modules.

Validation:

- Manual: inspect logs and trace records from representative runs.
- Automated: tests for required log fields or trace persistence hooks where practical.
- CI/CD maturity: add metrics endpoint and structured logging contract checks.

## Phase 6: Local Kubernetes and Helm

Goal:
Run the platform locally on Kubernetes using real Kubernetes objects first, then package the deployment with Helm.

Core tasks:

- Create a local `kind` Kubernetes cluster setup.
- Add raw Kubernetes manifests for API, PostgreSQL, config, secrets, services, and migration jobs.
- Add health/readiness probes for the API.
- Add a Kubernetes migration job that runs Alembic against PostgreSQL.
- Convert the working manifests into a Helm chart with explicit values.
- Document local cluster creation, install, upgrade, rollback, and teardown.
- Keep Kubernetes manifests and Helm values aligned with application environment contracts.

Exit conditions:

- A fresh local Kubernetes cluster can run the API and PostgreSQL.
- Alembic migrations can run from inside the cluster.
- The API is reachable through port-forwarding or an ingress-like local path.
- The Helm chart can install, upgrade, and uninstall the stack without manual object edits.
- Helm packages the Kubernetes deployment without hiding the underlying Kubernetes resources from review.

Validation:

- Manual: create a local cluster, deploy raw manifests, then deploy through Helm and smoke test `/health`, `/ready`, and `/metrics`.
- Automated: render Helm templates and validate Kubernetes manifests where practical.
- CI/CD maturity: add Kubernetes manifest validation and Helm template rendering checks.

## Phase 7: Argo CD GitOps

Goal:
Deploy the local Kubernetes stack through Argo CD so Git becomes the source of truth for application deployment.

Core tasks:

- Install Argo CD into the local Kubernetes cluster.
- Add an Argo CD Application for the Helm chart.
- Define environment-specific values for local development.
- Document sync, diff, rollback, and drift inspection workflows.

Exit conditions:

- Argo CD can deploy the application from the repository.
- A Helm value change in Git is visible as an Argo CD diff and can be synced.
- Rollback and drift inspection are documented and manually validated.

Validation:

- Manual: sync the app through Argo CD, change a value, inspect diff, sync again, and verify the deployed API.
- Automated: validate Argo CD Application manifests where practical.
- CI/CD maturity: add Argo CD Application manifest validation, but keep sync/apply as a manual local workflow.

## Phase 8: AWS Terraform Low-Cost Deployment

Goal:
Deploy the platform to AWS with Terraform while staying close to free or low-cost and avoiding unnecessary managed infrastructure.

Default deployment strategy:

- Use ECR for container images.
- Use GitHub Actions OIDC for AWS authentication.
- Use Lambda container image plus API Gateway as the first low-idle-cost runtime.
- Keep ECS Fargate as an optional later learning track.
- Do not use EKS in the default path because it is not close to free.
- Defer managed PostgreSQL until there is a clear cost and persistence decision.

Core tasks:

- Add Terraform modules for ECR, IAM/OIDC, API runtime, logs, and required networking.
- Add image build and push flow for the API container.
- Add Terraform validation and plan workflows.
- Add deployment smoke tests and teardown instructions.
- Add cost guardrails and document which resources may create charges.

Exit conditions:

- Terraform can create the low-cost AWS runtime from a clean state.
- The API image can be pushed to ECR.
- The deployed endpoint responds to health/version checks.
- Logs are visible in CloudWatch.
- Teardown returns the account close to zero ongoing cost.

Validation:

- Manual: run `terraform fmt`, `terraform validate`, review `terraform plan`, apply to a sandbox account, smoke test, and destroy.
- Automated: CI validates Terraform formatting and plans without applying by default.
- CI/CD maturity: add Terraform format, validate, and plan checks; cloud apply requires explicit approval.

## Phase 9: CI/CD Release Gates and Promotion

Goal:
Harden the CI/CD work accumulated across earlier phases into a coherent release and promotion system.

CI/CD is not introduced here from scratch. It grows gradually:

- Phase 1: lint, compile/import, PostgreSQL, Alembic, and ingestion tests.
- Phase 2: retrieval and vector-store checks.
- Phase 3: mocked LangGraph workflow checks.
- Phase 4: local evaluation smoke checks.
- Phase 5: observability contract checks.
- Phase 6: Kubernetes and Helm validation.
- Phase 7: Argo CD manifest validation.
- Phase 8: Terraform validation and non-applying plans.

Core tasks:

- Consolidate existing GitHub Actions into clear CI, image, infrastructure, and release workflows.
- Add release promotion rules for local, staging-like, and cloud targets.
- Add branch/tag rules, environment approvals, and secret requirements.
- Add controlled deployment workflows that require explicit approval for cloud apply.
- Document rollback and failed-release handling.

Exit conditions:

- Pull requests run meaningful quality gates.
- CI can test against PostgreSQL.
- Docker image builds in CI.
- Helm and Terraform checks run without applying infrastructure by default.
- Cloud deployment requires explicit approval and documented environment variables/secrets.
- Release promotion is documented and repeatable from a clean branch/tag.

Validation:

- Manual: inspect workflow output from a real branch or pull request.
- Automated: GitHub Actions pass for lint, tests, migrations, Docker build, Helm validation, and Terraform validation.

## Phase 10: MCP Research Tools

Goal:
Expose selected search, lookup, synthesis, workflow, and evaluation capabilities through MCP.

Core tasks:

- Define MCP tool contracts for the most useful research actions.
- Implement adapters from platform services to MCP-safe interfaces.
- Document tool behaviors and constraints.

Exit conditions:

- Selected platform capabilities are callable through MCP with stable contracts.
- Tool outputs are sufficiently structured for external clients.

Validation:

- Manual: invoke MCP tools against representative research tasks.
- Automated: contract tests for MCP tool input/output behavior.

## Phase 11: Production Hardening

Goal:
Add deployment, observability, authentication, and operational safety.

Core tasks:

- Harden deployment packaging, Kubernetes configuration, and AWS environment configuration.
- Add production-oriented auth, secret handling, and operational protections.
- Finalize release, rollback, observability, and incident-response practices.

Exit conditions:

- The platform can be deployed repeatably with documented operational steps.
- Production safety requirements are in place for configuration, auth, and deployment checks.
- Local Kubernetes, Argo CD, and AWS Terraform tracks have documented smoke tests and teardown paths.

Validation:

- Manual: deployment rehearsal and smoke test.
- Automated: CI/CD deployment checks, Kubernetes manifest checks, Helm validation, Terraform validation, and environment validation where applicable.
