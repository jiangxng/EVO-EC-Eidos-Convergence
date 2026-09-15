# G5 Adapter Certification — v0.2.0 to v0.2.1

Status: EXECUTABLE EVIDENCE REQUIRED

This document narrows the existing migration map into certifiable adapter obligations. It does not change frozen v0.2.0 contracts.

## A1 EvoIntelligenceFeedV010 -> Enterprise Observation

PRESERVED: enterprise identity, source business fact identity where available, correlation, provenance, fact payload.

TRANSFORMED: event identity becomes canonical observation identity; occurred/business time are mapped only when their source meaning proves the canonical effective/observed/published distinction.

DEFAULTED: none for authoritative time or tenant semantics.

UNSUPPORTED: using a state/current snapshot as a durable observation without explicit event/fact semantics.

FAIL CLOSED: ambiguous time semantics, missing tenant scope, cross-tenant payload, unverifiable source identity.

## A2 EvoOutcomeV010 -> Enterprise Observation outcome projection

PRESERVED: enterprise identity, proposal/correlation relationship, execution reference, outcome status, measures, provenance.

TRANSFORMED: outcome identity becomes observation identity only through an explicit adapter-generated observation envelope; adapter generation must be deterministic and idempotent.

DEFAULTED: observation type/version may be adapter constants declared by the profile.

UNSUPPORTED: EC lessons, interpretation or learned knowledge represented as EVO operational observation truth.

FAIL CLOSED: missing operational source/provenance or tenant mismatch.

## A3 EvoCommandProposalV010 -> Command Proposal

PRESERVED: proposal identity, enterprise scope, target command/capability intent, proposed input, rationale/evidence, correlation.

TRANSFORMED: legacy idempotency is separated from proposal identity; canonical command contract/input-schema versions must be resolved from EVO-published metadata rather than invented by EC.

DEFAULTED: none for authorization, command schema version or business authority.

UNSUPPORTED: legacy fields that imply trusted authorization result.

FAIL CLOSED: unknown/retired command version, expired proposal, proposal_id == command_idempotency_key, fake authorization claims, invalid proposed input.

## A4 EcExperienceProposalV010 -> Experience Proposal

PRESERVED: proposal identity, composition intent, context, capability intent where mappable.

TRANSFORMED: legacy composition is normalized into canonical Eidos capability/version and Stability/Integrity/Decision Experience semantics only through an Eidos-certified adapter.

DEFAULTED: deterministic standard fallback may be used only when declared by Eidos policy.

UNSUPPORTED: arbitrary renderer/code generation, EC-owned admissibility, business authorization/execution.

FAIL CLOSED OR DETERMINISTIC FALLBACK: unknown capability/version, integrity violation, missing mandatory evidence, accessibility violation, Shared Core override.

## A5 EidosActionRequestV010 -> Host-neutral ActionRequest

PRESERVED: interaction/action intent, actor context evidence, correlation, creation/occurrence time where semantics match.

TRANSFORMED: EVO-specific target semantics move out of the universal ActionRequest into a separately certified Host/EVO mapping profile. Confirmation becomes evidence, never authorization.

DEFAULTED: no business authorization fields.

UNSUPPORTED: trusted authorization claims or arbitrary executable code.

FAIL CLOSED: stale presented state/definition, tampered confirmation evidence, unsupported action contract/version.

## A6 ActionRequest -> EVO Action Mapping Profile

This is a profile, not Eidos core semantics.

PRESERVED: actor/delegation evidence, correlation/causation, action semantic, submitted values, idempotency intent where valid.

TRANSFORMED: Host maps the neutral action into an EVO-published public Command contract and input schema.

DEFAULTED: no authorization result. EVO re-authorizes at admission/execution time.

UNSUPPORTED: direct EVO database/internal service writes.

FAIL CLOSED: no public Command mapping, stale state, revoked delegation, schema mismatch, tenant mismatch.

## Certification Rule

A1-A6 remain NOT CERTIFIED until golden + invalid fixtures and provider/consumer/adapter tests prove the rules above. Documentation alone is not certification.
