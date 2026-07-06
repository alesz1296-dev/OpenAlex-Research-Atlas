# Cloud Lab Portfolio

Cloud Lab Portfolio is a lightweight, creative study app designed as a hands-on learning playground for Kubernetes, Terraform, and AWS SAA preparation.

The app presents a set of practice challenges such as:

- Kubernetes: Deployments, Services, ConfigMaps, Secrets, Probes, and RBAC
- Terraform: Networking, storage, and security resources
- AWS SAA: Core services, identity, and resilient architecture ideas

The goal is not to build a large product. The goal is to make the repository feel like a real platform engineering lab with a simple service, infrastructure as code, and deployment automation.

## Project goals

- Demonstrate Kubernetes fundamentals with local deployment
- Show Terraform-based infrastructure provisioning
- Practice DevOps workflows with containerization and automation
- Keep the app simple enough to understand quickly

## Suggested learning themes

- CKA-focused topics: Pods, Deployments, Services, ConfigMaps, Secrets, Probes, Namespaces, RBAC
- Terraform-focused topics: providers, variables, resources, outputs, state, modules
- AWS SAA-focused topics: VPC, security groups, IAM, S3, networking, availability and resilience

## Quick start

Run locally:

```bash
python app/main.py
```

Then open:

- http://localhost:8080/
- http://localhost:8080/health
- http://localhost:8080/api/challenges
```
