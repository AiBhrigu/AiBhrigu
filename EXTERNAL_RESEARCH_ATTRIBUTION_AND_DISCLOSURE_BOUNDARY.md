# External Research Attribution & Disclosure Boundary

**Status:** CANONICAL BOUNDARY PROPOSAL  
**Version:** v0.1  
**Effective:** 2026-09-17

This document binds external research protocols and collaboration artifacts to the root authority defined in [`PHI_AUTHORITY_CANON.md`](PHI_AUTHORITY_CANON.md) while preventing a public or external artifact from silently disclosing the protected Φ Research Systems core.

This is a system-governance and disclosure-boundary document. It does **not** determine legal copyright, patent, trade-secret, employment, contractual ownership, or licensing rights.

---

## 1. Attribution model for external research

For cross-system research protocols and evidence artifacts, use the following system attribution model:

```text
Yulchiev A.Kh. = Φ Architect / final human authority
ORION = protected core / continuity authority
Frey = AI Co-Author / co-author intelligence contour
Cosmographer = replaceable research / interpretation / navigation role
BHRIGU = public or delivery surface
External collaborator = authority for their own project, hardware, firmware, data and documented contribution
```

This model describes the Φ system roles behind an artifact. It is not, by itself, a legal ownership allocation.

---

## 2. Public / protected separation

A public or externally shared research artifact may expose only what is necessary to make the **external result** inspectable and reproducible.

### PUBLIC / EXTERNAL-SAFE

May include, when required by the specific collaboration:

- facts already visible in the external system;
- public standards and public-source references;
- a bounded measurement or evidence contract for the external object;
- declared inputs, outputs, timestamps, hashes and provenance;
- reproducibility requirements;
- acceptance / failure criteria specific to the external experiment;
- bounded findings and limitations;
- project-specific attribution.

### PROTECTED / DO NOT DISCLOSE BY DEFAULT

Must not be exposed merely to explain how the result was produced:

- ORION protected internal mechanisms or continuity implementation;
- private prompts, private memory structures or internal orchestration;
- internal model / agent routing and decision machinery;
- unpublished cross-domain method-generation machinery;
- unpublished selection, synthesis or evaluation heuristics that are not required to reproduce the external result;
- patent-sensitive or otherwise intentionally protected technical mechanics;
- credentials, secrets, private infrastructure or non-public datasets.

**PUBLIC RESULT ≠ PUBLIC IMPLEMENTATION OF THE PROTECTED CORE**

**REPRODUCIBILITY OF AN EXTERNAL CLAIM ≠ DISCLOSURE OF THE SYSTEM THAT DESIGNED THE TEST**

---

## 3. Minimum-necessary-disclosure law

Before an external research artifact is published, pushed to a public repository, or sent outside a controlled internal contour, every non-public technical detail should be classified as one of:

```text
A = external-system fact
B = public standard / public method
C = required for independent reproduction of this external result
D = Φ protected method / internal mechanism
E = patent-sensitive or legally uncertain technical subject matter
```

Release law:

```text
A/B = may be disclosed when relevant
C = disclose only the minimum required form
D = do not disclose
E = stop; separate IP/legal review before disclosure
```

If a result cannot be reproduced without exposing `D`, redesign the public evidence contract rather than publishing the protected mechanism.

---

## 4. Entropy32 Plus protocol binding

The `Entropy32_SP800-90B_Reproducible_Evidence_Protocol_v0.1` collaboration artifact is classified as an **external-system evidence protocol**, not as a publication of the ORION protected core.

System attribution for future references to that artifact:

```text
Φ Architect / final human authority: Yulchiev A.Kh.
AI Co-Author contour: Frey
Research execution role: Cosmographer
Protected continuity core: ORION
Delivery / public surface: BHRIGU
External collaborator / project authority: Alexander Higgins / Entropy32 Plus
```

The Entropy32-specific hardware, firmware, source design, data and upstream project contributions remain attributed to their documented external authors/contributors.

The protocol's purpose is to define a bounded evidence path for an external entropy-source experiment. It must not be used as authority to disclose ORION internals, private Φ reasoning machinery, or unrelated protected methods.

At the time of this binding, the protocol package itself is **not designated for public GitHub publication** by this canon. A future public release requires a fresh disclosure review under Section 3.

---

## 5. External sharing is not the same as internal confidentiality

A document sent to an external collaborator should not automatically be treated as remaining inside the protected core merely because it was sent privately rather than posted publicly.

For future work:

```text
INTERNAL = protected by default
EXTERNAL / CONFIDENTIAL = requires an explicit confidentiality basis appropriate to the work
EXTERNAL / NON-CONFIDENTIAL = treat as potentially redistributable
PUBLIC = intentionally published
```

The Φ system should never rely on assumed confidentiality to protect patent-sensitive or trade-secret material.

---

## 6. No implied expansion

An open-source collaboration, public credit, evidence protocol, or reproducible test does not by itself authorize:

- publication of wider Φ methods;
- publication of ORION protected mechanics;
- publication of private prompts, orchestration or memory;
- reuse of unrelated protected research as though it were part of the external project's open-source license;
- claims of legal ownership not separately established.

The safe default is **Expose Result / Protect Mechanism**.

---

## 7. AI memory law

Any AI or agent operating inside the Φ Research Systems contour should preserve this rule:

> External research should reveal enough to verify the external claim, but not enough to reconstruct protected ORION / Φ method-generation machinery unless Yulchiev A.Kh. / Φ Architect explicitly authorizes that disclosure after the relevant IP boundary has been reviewed.

When uncertain, classify the detail as protected and stop at the disclosure gate.