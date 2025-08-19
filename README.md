# Temporal Indirection Pattern

An Ontology Design Pattern (ODP) for representing persistent identifiers that maintain stable identity while their referents change over time according to defined rules.

## Overview

The Temporal Indirection Pattern models situations where stable references point to different entities over time through rule-based transitions. This pattern is fundamental to systems where stable identifiers must persist while their underlying implementations change systematically.

### Key Concepts

- **Persistent Reference**: A stable identifier that maintains its identity over time
- **Referent Entity**: The actual entity being referenced at any given time
- **Temporal Binding**: The relationship linking a reference to an entity for a specific period
- **Transition Event**: The moment when one referent changes to another
- **Resolution Context**: The rules and conventions governing the temporal indirection

## Pattern Motivation

Temporal indirection occurs when a persistent identifier maintains stable identity while its referent—the entity it denotes—changes over time according to systematic rules. This creates a two-level reference system: the stable identifier at one level, and the changing referent at another, mediated by time-dependent mapping rules.

### Real-World Applications

#### Financial Markets
Generic tickers like "CL1" (front-month crude oil futures) maintain stable identity while referencing different monthly contracts as they roll. This enables:
- Continuous price tracking across contract transitions
- Automated trading strategies without reconfiguration
- Historical analysis with consistent identifiers

#### Aviation Operations
Flight numbers like "UA001" persist while aircraft, crews, and routes change daily, supporting:
- Performance metrics aggregation
- Safety investigation reconstruction
- Maintenance tracking across fleet rotations
- Regulatory compliance reporting

#### Other Domains
- **Healthcare**: On-call physician roles, shift assignments, clinical trial protocols
- **Transportation**: Shipping routes, vehicle fleet management
- **Manufacturing**: Production line assignments, supplier rotations
- **Environmental Monitoring**: Sensor station assignments, satellite observation slots
- **Digital Services**: API endpoint versions, load-balanced server assignments

## Repository Structure
```
temporal-indirection-pattern/
├── README.md
├── requirements.txt
├── ontologies/
│   ├── temporal-indirection-pattern.ttl        # Core pattern definition
│   ├── temporal-indirection-pattern-dul.ttl    # DUL-aligned version
│   ├── financial-derivatives-ontology.ttl      # Financial domain specialization
│   └── aviation-operations-ontology.ttl        # Aviation domain specialization
├── data/
│   ├── derivatives-instances.ttl               # Financial market instances
│   └── aviation-instances.ttl                  # Aviation operations instances
├── queries/
│   ├── derivatives-competency-questions.sparql # Financial pattern queries
│   └── aviation-competency-questions.sparql    # Aviation pattern queries
└── tests/
├── test_pattern_derivatives.py                 # Financial pattern tests
└── test_pattern_aviation.py                    # Aviation pattern tests
```

## Installation

### Requirements
- Python 3.8+
- RDFLib for RDF/OWL processing
- SPARQL support

### Setup
```bash
# Clone the repository
git clone https://github.com/YuliaS/temporal_indirection.git
cd temporal-indirection-pattern

# Install dependencies
pip install -r requirements.txt
```

## Running Tests

### Financial Derivatives Tests
```bash
python tests/test_pattern_derivatives.py
```

Expected output:
```txt
Loading ontologies/temporal-indirection-pattern.ttl...
Loading ontologies/financial-derivatives-ontology.ttl...
Loading data/instances.ttl...
Total triples loaded: 400

============================================================
TEMPORAL INDIRECTION PATTERN TEST SUITE
============================================================

TEST RESULTS:
[Table showing all competency questions with PASS status]

Coverage: 100%
Status: ✓ ALL TESTS PASSED
```

### Aviation Operations Tests
```bash
python tests/test_pattern_aviation.py
```

Expected output:
```txt

Loading ontologies/temporal-indirection-pattern.ttl...
Loading ontologies/aviation-operations-ontology.ttl...
Loading data/aviation-instances.ttl...
Total triples loaded: 467

======================================================================
AVIATION TEMPORAL INDIRECTION PATTERN TEST SUITE
======================================================================

TEST RESULTS:
[Table showing all competency questions with PASS status]

AVIATION SAFETY & COMPLIANCE SUMMARY
✈ Flight Number Tracked: UA001
✈ Total Aircraft Rotations: 3
✈ Total Crew Rotations: 3
✈ Safety Incidents Recorded: 1
✈ Maintenance Events Tracked: 2
✈ Temporal Consistency: ✓ Verified

Coverage: 100%
Status: ✓ ALL TESTS PASSED
```

## Pattern Components

### Core Classes (Ontology)
- **ClassDescriptionPersistentReference**: Stable identifier maintaining identity over time  
- **ReferentEntity**: The actual entity being referenced  
- **TemporalBinding**: Links reference to entity for a time period  
- **TransitionEvent**: Marks change from one referent to another  
- **ResolutionContext**: Rules governing the temporal indirection  
- **Convention**: Domain-specific rules for transitions  
- **TransitionRule**: Specific rules triggering transitions  
- **Observation**: Observations linked to both reference and referent  
- **TemporalInterval**: Time period with start and end times  

### Core Properties
- **bindsTo**: TemporalBinding → ReferentEntity — Links binding to referent  
- **hasTemporalBinding**: PersistentReference → TemporalBinding — Links reference to bindings  
- **hasTransition**: ReferentEntity → TransitionEvent — Links entity to transitions  
- **hasValidTime**: TemporalBinding → TemporalInterval — Valid time period  
- **observedEntity**: Observation → PersistentReference — Persistent reference observed  
- **observedReferent**: Observation → ReferentEntity — Specific referent at observation  

### Competency Questions
The pattern addresses these fundamental questions:
- **Current State**: What is the current referent for a given persistent reference?  
- **Historical State**: What was the referent at a specific historical timestamp?  
- **Transitions**: When did referent transitions occur?  
- **Observations**: What observations are associated with specific referents?  
- **Complete History**: What is the complete history of referents?  
- **Transition Rules**: What rules triggered specific transitions?  
- **Temporal Consistency**: Are there gaps or overlaps in temporal bindings?  
- **Domain-Specific**: (Financial) Spread relationships, (Aviation) Safety investigations  

### Domain Implementations

#### Financial Derivatives
Demonstrates generic ticker persistence (CL1, CL2) for futures contracts:
- Monthly contract rolls  
- Calendar spread tracking  
- Price observation attribution  
- Exchange convention compliance  

#### Aviation Operations
Demonstrates flight number persistence (UA001) with changing operations:
- Daily aircraft rotations  
- Crew assignment tracking  
- Performance metrics aggregation  
- Safety incident investigation  
- Maintenance event correlation  

### SPARQL Query Examples

#### Get Current Referent
```sparql
SELECT ?referent WHERE {
    :PersistentID :hasTemporalBinding ?binding .
    ?binding :bindsTo ?referent ;
             :hasValidTime ?period .
    ?period :hasStartTime ?start ;
            :hasEndTime ?end .
    FILTER(NOW() >= ?start && NOW() < ?end)
}
```

#### Historical Reconstruction
```sparql
SELECT ?referent ?time WHERE {
    :PersistentID :hasTemporalBinding ?binding .
    ?binding :bindsTo ?referent ;
             :hasValidTime ?period .
    ?period :hasStartTime ?time .
    FILTER(?time <= "2024-08-14T12:00:00Z"^^xsd:dateTime)
}
ORDER BY DESC(?time) LIMIT 1
```

### Contributing
We welcome contributions! Please see our contributing guidelines for:
- Adding new domain specializations  
- Extending competency questions  
- Improving test coverage  
- Documentation enhancements  

#### Adding a New Domain
1. Create domain ontology in `ontologies/`  
2. Add instance data in `data/`  
3. Write competency questions in `queries/`  
4. Implement test suite in `tests/`  
5. Update documentation  

### Publications
For detailed pattern description and theoretical foundation, see:
- Paper Title: "An Ontology Design Pattern for Representing Temporal Indirection"  
  Authors: Yulia Svetashova  
  Conference/Journal: TBA
  Year: 2025 

### Use Cases

#### Financial Risk Management
- Track rolling futures positions  
- Maintain continuous price histories  
- Automate contract roll procedures  
- Calculate spread relationships  

#### Aviation Safety
- Reconstruct operational context for incidents  
- Track maintenance across fleet  
- Analyze crew performance patterns  
- Ensure regulatory compliance  

#### Healthcare Operations
- Manage on-call physician schedules  
- Track patient observations across shifts  
- Maintain treatment continuity  
- Audit clinical decisions  

### Related Patterns
- **Recurrent Situation Series**: For modeling periodic recurring situations  
- **Observation Pattern**: For linking observations to entities  
- **Time Indexed Situation**: For situations with temporal extent  
- **Role Pattern**: For modeling roles independent of their players  

### Contact
- **Issues**: [GitHub](https://github.com/YuliaS/temporal_indirection/issues)  
- **Email**: svetashova@gmail.com  
- **Pattern Portal**: [OntologyDesignPatterns.org](http://OntologyDesignPatterns.org)  

### Citation
If you use this pattern in your research, please cite:
```bibtex
@inproceedings{temporal-indirection-2024,
  title={An Ontology Design Pattern for Temporal Indirection},
  author={Svetashova, Yulia},
  booktitle={TBA},
  year={2025},
  pages={xx-xx}
}
```