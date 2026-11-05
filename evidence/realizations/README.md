# Evidence realization descriptions

This directory holds immutable, versioned descriptions of concrete realizations assessed under EBP §1.4.

Each realization description MUST identify:

- the SLC implementation and immutable version or commit;
- the substrate and relevant component identities;
- the configuration identity or digest;
- deployment assumptions and declared scope;
- the assurance claim(s) and the realization elements on which each claim depends;
- the applicable adversary model and guarantee, where an EBP assessment is made.

A record MUST reference a specific immutable version and content digest, not a mutable filename alone. When a referenced element changes materially, the affected assurance claim requires reassessment.

Do not create a realization description by guessing missing deployment facts. Until the tuple is documented and its immutable identity can be cited, evidence records use `realization: not-established`.

This file is guidance only. It does not describe or establish a concrete EBP realization.
