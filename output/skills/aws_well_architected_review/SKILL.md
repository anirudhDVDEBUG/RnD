---
name: AWS Well-Architected Review
description: |
  Apply AWS Well-Architected Framework best practices to cloud infrastructure and application code.
  TRIGGER: When reviewing AWS architecture, designing cloud infrastructure, checking for Well-Architected compliance, evaluating security/reliability/cost/performance of AWS workloads, or preparing for an AWS Well-Architected Review.
---

# AWS Well-Architected Review

Apply the AWS Well-Architected Framework pillars to evaluate and improve cloud architecture decisions in code and infrastructure.

## When to use

- "Review this architecture for AWS best practices"
- "Is this infrastructure Well-Architected?"
- "Check this AWS deployment for security and reliability issues"
- "Help me apply the Well-Architected Framework to this design"
- "Optimize this cloud architecture for cost and performance"

## How to use

### Step 1: Identify the workload scope

Determine which AWS services, infrastructure-as-code templates (CloudFormation, CDK, Terraform), and application code are part of the workload under review.

### Step 2: Evaluate against the six pillars

Review the architecture against each Well-Architected pillar:

1. **Operational Excellence** — Are there runbooks, observability (CloudWatch, X-Ray), CI/CD pipelines, and IaC? Are operations automated?
2. **Security** — Is least-privilege IAM enforced? Are secrets managed (Secrets Manager/Parameter Store)? Is encryption at rest and in transit configured? Are security groups and NACLs properly scoped?
3. **Reliability** — Are there multi-AZ deployments, auto-scaling, health checks, backup/recovery strategies, and circuit breakers?
4. **Performance Efficiency** — Are the right instance types/services selected? Is caching used (ElastiCache, CloudFront)? Are databases properly indexed?
5. **Cost Optimization** — Are resources right-sized? Are Reserved Instances or Savings Plans considered? Are unused resources identified? Is lifecycle management configured for S3?
6. **Sustainability** — Are resources efficiently utilized? Is the architecture minimizing waste and carbon footprint?

### Step 3: Generate findings and recommendations

For each pillar, produce:
- **Finding**: Describe the current state and gap
- **Risk level**: High / Medium / Low
- **Recommendation**: Specific, actionable improvement with code examples where applicable
- **AWS best practice reference**: Link to the relevant Well-Architected lens or documentation

### Step 4: Prioritize remediation

Rank findings by risk level and implementation effort. Provide concrete code changes (IaC patches, policy documents, configuration updates) for high-priority items.

## Key patterns to check

- IAM policies with `*` resources or actions
- Security groups with `0.0.0.0/0` ingress on non-HTTP ports
- Single-AZ deployments for production workloads
- Missing encryption configuration on S3 buckets, RDS, EBS
- No auto-scaling or fixed capacity for variable workloads
- Missing CloudWatch alarms and dashboards
- Hard-coded secrets in code or environment variables
- No backup or disaster recovery plan
- Over-provisioned resources (instance sizes, provisioned IOPS)

## References

- Source: https://github.com/aws-samples/sample-well-architected-skills-and-steering
- AWS Well-Architected Framework: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
