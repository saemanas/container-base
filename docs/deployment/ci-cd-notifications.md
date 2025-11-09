# CI/CD Notification Templates

## Overview
- Channel: Operations email distribution list (GitHub notifications alias)
- Audience: Organization Admins, Site Operators, Compliance Leads
- Requirements: Notify on success, failure, rollback per `specs/002-cicd-hardening/spec.md` FR-012.

## Success Template
```
Subject: [CI/CD][SUCCESS] ${service} ${environment} run ${workflow_run_url}
Body:
- Service: ${service}
- Environment: ${environment}
- Tag/Commit: ${ref}
- Duration: ${duration}
- Evidence: ${artifact_url}
```

## Failure Template
```
Subject: [CI/CD][FAILURE] ${service} ${environment} run ${workflow_run_url}
Body:
- Failed Stage: ${stage_name}
- Error Summary: ${error_excerpt}
- Next Steps: Retry job or open incident
- Evidence: ${artifact_url}
```

## Rollback Template
```
Subject: [CI/CD][ROLLBACK] ${service} ${environment} triggered for ${rollback_tag}
Body:
- Triggered By: ${initiator}
- Rollback Tag: ${rollback_tag}
- ETA to Completion: ≤10 minutes
- Logs: ${artifact_url}
```

## Operational Checklist
- [ ] Attach CI summary artifact (`ci-summary-<run_id>`) to email
- [ ] Include Supabase RLS log link when migrations run
- [ ] Archive email in compliance folder within 24 hours
