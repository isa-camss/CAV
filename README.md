# Core Assessment Vocabulary (CAV)

[![License](https://img.shields.io/badge/License-EUPL%201.2-blue.svg)](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)
[![Latest Release](https://img.shields.io/badge/version-1.3.0-green.svg)](https://interoperable-europe.ec.europa.eu/collection/common-assessment-method-standards-and-specifications-camss/solution/core-assessment-vocabulary-cav)

## 📋 Overview

The **Core Assessment Vocabulary (CAV)** is a CAMSS Vocabulary that represents and defines what an “Assessment” of “assets” is and how to perform the assessment based on “Criteria”. It is a domain-agnostic vocabulary, meaning that it can be used to assess any type of assets. 

CAV is a specification that assures and controls quality of data and information at the basis of standards and specifications for the design and development of interoperable systems supporting Digital Public Services.

## 🎯 What Problem Does CAV Solve?

Organisations constantly need to assess various assets—from technical standards and software solutions to policies, services, and processes. However, these assessments are typically:
- Documented in inconsistent formats
- Difficult to compare across different contexts
- Hard to automate or integrate with other systems
- Locked in proprietary formats without semantic meaning
- Not easily shareable or reusable across organisations

CAV addresses these challenges by providing:

✅ **Universal assessment framework** that works for any type of asset  
✅ **Structured criteria definition** with evidence-based evaluation  
✅ **Machine-readable format** enabling automated processing and analysis  
✅ **Semantic interoperability** through reuse of established vocabularies  
✅ **Traceability** from reference frameworks through criteria to outcomes  

## 🚀 Key Use Cases

#### 1. **Standards and Specifications Assessment (CAMSS)**
The primary use case driving CAV development.

#### 2. **Digital Solution Assessment**
For assessing software systems and platforms.

#### 3. **Public Service Assessment**
For evaluating digital public services.

#### 4. **Policy and Governance Evaluation**
For organisational and policy assessments.

#### 5. **Knowledge Management and Decision Support**
For organisational learning and improvement.

#### 6. **Research and Academia**
For structured evaluation in research contexts.

## 🏗️ Architecture and Design Principles
CAV is built on two fundamental principles.

### 1. **Consistent Reuse**
Respect and reuse already existing and commonly agreed interpretation of concepts and ontologies (e.g., DCAT, CCCEV, FOAF etc.), thus facilitating semantic interoperability. The methodological approach followed for the development of the CAV reuses the following ontologies and vocabularies:
- **Data Catalogue Vocabulary (DCAT)**
- **Friend of a Friend (FOAF)**
- **Asset Description Metadata Schema (ADMS)**
- **The Organization Ontology**
- **Core Criterion and Core Evidence Vocabulary (CCCEV)**
- **DCMI Metadata Terms (DCTerms)**
- **Schema.org**

### 2. **Separation of Concerns**
Isolate technical and business limitations and rules as much as possible to ensure flexibility and cost-saving quality of the implementation and maintenance of the “core” vocabulary.

## 📦 What's in This Repository

This repository contains the formal specification and implementation files for CAV:

```
CAV/
├── cav_html/                             # The CAV in HTML format.
├── doc/                                  # Specification documents and guides.
│   ├── CAMSS_info v9.0.0.pdf           # Set of informative documents about CAMSS.
│   ├── CAV_Specification v1.3.0.pdf    # The CAV v1.3.0 specification in pdf format.
│   ├── CAV v1.3.0 Release Notes.pdf    # The CAV release notes.
│   └── EUPL v1.2.pdf                   # EUPL v1.2 license.
├── ttl/                                  # The CAV in ttl format.
│   └── cav_tbox.ttl                    # The CAV in RDF format.
│── uml                                   # The CAV UML.
│   ├── CAV_UML_v1.2.0.xml              # The CAV UML in xml format.
│   ├── CAV_UML_1.3.0.drawio              # The CAV UML in drawio format.
│   └── CAV_UML_v1.3.0.png              # The CAV UML in png format.
├── README.md                             # The github readme of the CAV.
└── cav.ttl                               # The CAV in RDF format.
```

## 🌍 Relationship to Other Initiatives

### CAMSS (Common Assessment Method for Standards and Specifications)
CAV supports Digital Europe's goals for interoperable digital public services through structured assessment capabilities.

### SEMIC
CAV is one of the core vocabularies, alongside other vocabularies developed by SEMIC.

## 📚 Additional and Learning Resources

- **CAV on Interoperable Europe Portal**: [Core Assessment Vocabulary (CAV)](https://interoperable-europe.ec.europa.eu/collection/common-assessment-method-standards-and-specifications-camss/solution/core-assessment-vocabulary-cav)
- **CAV in HTML format**: [CAV Vocabulary in HTML](https://isa-camss.github.io/CAV/index-en.html)
- **CSSV on Interoperable Europe Portal**: [Core Standards and Specifications Vocabulary (CSSV)](https://interoperable-europe.ec.europa.eu/collection/common-assessment-method-standards-and-specifications-camss/solution/core-standards-and-specifications-vocabulary-cssv)
- **CAMSS Welcome Page**: [CAMSS on Interoperable Europe](https://interoperable-europe.ec.europa.eu/collection/common-assessment-method-standards-and-specifications-camss)
- **"Introduction to Core Vocabularies" course**: [Core Vocabularies course on Interoperable Europe Academy](https://academy.europa.eu/courses/introduction-to-core-vocabularies)

## 📄 License

CAV is released under the **European Union Public Licence (EUPL) v1.2**.

You are free to use, modify, and distribute this vocabulary in accordance with the EUPL terms. See the [LICENSE](https://eupl.eu/1.2/en/) file for details.

## 🤝 Contributing

CAV has been developed through public consultation with input from various stakeholders. We welcome feedback and contributions:

1. **Report Issues**: Use GitHub Issues to report bugs, suggest improvements, or request clarifications
2. **Discuss Use Cases**: Share your implementation experiences and domain-specific needs
3. **Submit Changes**: Fork the repository and submit pull requests for enhancements
4. **Extend for Your Domain**: Create domain-specific extensions and share your approach

## 📧 Contact

For questions, feedback, or collaboration opportunities:
- Open an issue in this repository
- Visit the [Interoperable Europe Portal](https://interoperable-europe.ec.europa.eu/)
- Contact the CAMSS team through official channels
- Join the CAMSS community discussions

## 🔄 Version History

- **v1.3.0** (Latest): Enhanced metadata and improved alignment with DCAT
- **v1.2.0**: Extended assessment statement capabilities
- **v1.1.0**: Added support for evidence chains and criterion grouping
- **v1.0.0**: First stable release
- **v1.0.0 Beta**: Initial public consultation release

See the full release history [here](https://interoperable-europe.ec.europa.eu/collection/common-assessment-method-standards-and-specifications-camss/solution/core-assessment-vocabulary-cav/releases)

---

**Maintained by**: ISA² Programme / Interoperable Europe  
**Last Updated**: 2026  
**Status**: Active development and maintenance
