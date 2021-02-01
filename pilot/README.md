# CAV Pilot 1

This folder contains the development of an Application Profile of the CAV (a CAV-AP). The objective of this pilot is focused on 
testing whether the CAV is suitable for extension and customization in a domain-specific environment.

The pilot was suggested by an Italian Public Administration (Anticorruzione) interested in studying how CAV can be connected to the comparative assessment 
of tenders based on MEAT Award Criteria. The business domain, thus, is Public Procurement in the European Union.

For the development of this CAV-AP, the latest version of the [ePO](https://github.com/eprocurementontology/eprocurementontology/wiki) was used. ePO is being 
maintained by the Publications Office of the European Union, and the latest available version is 2.0.2 (soon to be released on the 
[EU Vocabularies](https://op.europa.eu/en/web/eu-vocabularies) site).

All the materials used and developed in the context of this pilot are organised in this folder as follows:

- **doc**: documentation explaining how Anticorruzione use existing multicriteria methods for the decision-making process;
- **py**: python3 scripts for the extraction of data from the sample dataset provided, its transformation and loading as RDF. It contains also a Jupyter Notebook illustrating the logic of the pilot;
- **uml**: the data model illustrating how this CAV-AP builds extensions and custiomisation on top of the CAV, and how it is connected to ePO and other vocabularies. The model is browseable as HTML;
- **xmi**: the exportation of the UML model using the automated tools developed in the context of ePO.

