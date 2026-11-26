# Trace Model

The kinds of work products of the product line and the links between them. Each arrow points from a
work product to the one it links up to, and is named by its link.

A feature is not a level of the chain and has no trace links. The feature model is built from the
customer requirements: it holds a feature only where customers differ, to give the product line its
variation points and so support different variants. The function itself, like blinking, has its own
requirements. A variant selects features in its `config.txt`.

A feature switches every kind of work product except the customer requirements: through its condition
in the pages (Jinja), in the code (`#if CONFIG_<FEATURE>`) and in the tests, a variant has exactly the
software requirements, hazards, safety goals, architecture elements, specs, code and tests of its
features. A customer requirement belongs to the customer of a variant and is never switched by a
feature.

A detailed design spec refines the architecture element of its component. When a software requirement
lies entirely inside one component, the spec also realises it directly.

```{mermaid}
%%{init: {"theme": "default"}}%%
flowchart BT
    CR["Customer requirement"]
    subgraph SWITCHED["Switched by features through their conditions"]
    SWR["Software requirement<br/>(a function)"]
    ARCH["Architecture element<br/>(component, interface)"]
    DD["Detailed design (spec)"]
    IMPL["Implementation"]
    HAZ["Hazard"]
    SG["Safety goal"]
    SR["Safety requirement<br/>(a software requirement)"]
    VT["Variant test spec"]
    UT["Unit test spec"]
    RES["Test result"]
    end
    VAR["Variant"]
    FEAT["Feature<br/>(only to toggle or set)"]

    SWR -->|satisfies| CR
    ARCH -->|realises| SWR
    DD -->|refines| ARCH
    DD -->|realises| SWR
    DD -->|realises| SR
    IMPL -->|implements| DD
    HAZ -->|arises from| SWR
    SG -->|mitigates| HAZ
    SR -->|satisfies| SG
    ARCH -->|realises| SR
    VAR -->|selects| FEAT
    VT -->|tests| SWR
    UT -->|tests| DD
    VT -->|results| RES
    UT -->|results| RES

    classDef safety fill:#FAECE7,stroke:#993C1D,color:#712B13
    classDef variability fill:#E1F5EE,stroke:#0F6E56,color:#085041
    class HAZ,SG,SR safety
    class VAR,FEAT variability
```
