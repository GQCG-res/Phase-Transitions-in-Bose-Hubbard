<p align="center">
<img src="../media/outline.png" width="400">
</p>

# <G|QC|G> outlines

As [explained by George Whitesides](../media/whitesides.pdf), an _outline_ is a system for planning your in-progress research. It consists of carefully orga­nized and presented data, with attendant objectives, hypotheses, and conclusions.

An outline itself contains little text as it will be rewritten many times throughout the course of your research as part of our continuous effort to un­derstand, analyze, summarize, and reformulate hypotheses on paper. In order to manage our research projects, we augment each outline with a ZenHub project board that gives an overview of current and planned issues in a [Kanban-like framework](https://www.atlassian.com/agile/kanban).

## Content of template repo

This template repo consists of:
* [`code`](code/README.md) - All code that is required to reproduce the results of this project.
* [`data`](data/README.md) - All input/output data that is relevant to this project.
* [`outline`](outline/README.md) - The actual <G|QC|J> outline.
* [`notes`](notes/README.md) - A set of notes that explain context and background of this research notes.

## Devcontainers / Docker

The `outline` folder contains its own `.devcontainer`, such that you should be able to compile the outline on your infrastructure by opening **only** the `outline` folder in VS Code. (When opening the `outline` folder in VS Code, it will prompt you to re-open the folder in that container.) Similarly, the `notes` folder also contains its own `.devcontainer`.

We urge you to design a separate `.devcontainer` for the source code you've written, such that all members involved in your research can reproduce your results on their infrastructure.

## GitHub Actions

This repo is under [CI/CD with Github Actions](https://github.com/features/actions). As such, each contributing member should be able to download the latest version of your outline and notes by clicking on the green :heavy_check_mark: next to that commit > Details > Artifacts (top right) > Download artifacts. 

# Publishing matured outlines

<p align="center">
<img src="../media/writing.png" width="400">
</p>

After your outline has matured through *multiple* iterations it will become evident when your outline has reached the stage where you would like to let the world know about your research.

> We note that turning your outline into a *published* paper can be a *very* long process, in which you have to take all the points of view of your co-authors and reviewers into account over many iterations. Don't let this discourage you; after all, the task of a paper is to influence the direction of the field. It is the job of everyone in the field to critically analyze your thoughts so that we all agree on the directions taken (and run less risk of going in the wrong direction).

As optimizing the structure of a scientific paper requires a certain degree of skill and proficiency, please *return* to the following resources *regularly* while iterating on your paper: 
- [publishing your research](https://publish.acs.org/publish/author_university)
- [the art of scientific publications](https://pubs.acs.org/page/vi/art_of_scientific_publication.html)
- [how to produce first-class papers](../media/write-stuff.pdf)
- [elements of Science style](../media/elements-style.pdf)
- [Strunk and White](https://en.wikipedia.org/wiki/The_Elements_of_Style)

As your outline already contains the backbone of your research, you can start by exploring the [writing template](phd-proofreaders/writing-template.pdf) to see how the different elements of your paper fit together (which is essentially a mini-thesis in itself). Make sure you are discussing everything you need to, in the right way and at the right time. For every section, there is a cheat sheet and a work sheet (from https://www.thephdproofreaders.com/) and a set of comments from the perspective of the group.

| Section | Cheat sheet | Work sheet | Comments |
| --- | --- | --- | --- |
| Abstract | [Abstract](phd-proofreaders/cheat-sheets/abstract.pdf) | [Abstract](phd-proofreaders/worksheets/abstract.pdf) | [abstract](#abstract) | 
| Introduction | [Introduction](phd-proofreaders/cheat-sheets/introduction.pdf) & [Literature review](phd-proofreaders/cheat-sheets/literature.pdf) | [Introduction](phd-proofreaders/worksheets/introduction.pdf)  & [Literature review](phd-proofreaders/worksheets/literature.pdf) |
| Theoretical framework | [Theory](phd-proofreaders/cheat-sheets/theory.pdf) | [Theory](phd-proofreaders/worksheets/theory.pdf) |
| Methodology | [Methods](phd-proofreaders/cheat-sheets/methodology.pdf) | [Methods](phd-proofreaders/worksheets/methodology.pdf) |
| Results and discussion | [Results](phd-proofreaders/cheat-sheets/results.pdf) | [Results](phd-proofreaders/worksheets/results.pdf) |
| Conclusions | [Conclusions](phd-proofreaders/cheat-sheets/conclusions.pdf) | [Conclusions](phd-proofreaders/worksheets/conclusions.pdf) |

## Abstract 

A good abstract describes (in order) the **context/introduction to the field [1]**, **problem/why [2]**, **solution/how [3]**, **what [4]** and an **outlook [5]** (also see [How to construct a Nature summary paragraph](../media/nature-abstract.pdf)). The following (annotated) abstract illustrates these guidelines:

> Photoinduced charge-transfer is an important process in nature and technology and is responsible for the emergence of exotic functionalities, such as magnetic order for cyanide-bridged bimetallic coordination networks [1]. Despite its broad interest and intensive developments in chemistry and material sciences, the atomic-scale description of the initial photoinduced process, which couples intermetallic charge-transfer and spin transition, has been debated for decades; it has been beyond reach due to its extreme speed [2]. Here we study this process in a prototype cyanide-bridged CoFe system by femtosecond X-ray and optical absorption spectroscopies, enabling the disentanglement of ultrafast electronic and structural dynamics [3]. Our results demonstrate that it is the spin transition that occurs first on the Co site within ~50 fs, and it is this that drives the subsequent Fe-to-Co charge-transfer within ~200 fs [4]. This study represents a step towards understanding and controlling charge-transfer-based functions using light [5].

# Submitting to a journal

## Which journal should I submit to?

### Main journals

- [PCCP](https://www.rsc.org/journals-books-databases/about-journals/pccp/) - focused on important results in the area of physical chemistry. When to choose this journal?: key chemical insights based on analyses from quantum chemical data.
- [JCTC](https://pubs.acs.org/journal/jctcce) - focused new theories, methodology, and/or important applications in quantum electronic structure, molecular dynamics, and statistical mechanics. When to choose this journal?: novel quantum chemical theories / algorithms aimed at the developer community.
- [JCC](https://onlinelibrary.wiley.com/journal/1096987x) - concerned with all aspects of computational chemistry. When to choose this journal?: computational studies that apply existing techniques in new context.
- [JPC-A](https://pubs.acs.org/journal/jpcafh) - focuses on novel tools and methods in experiment and theory. When to choose this journal?: new tools or methods that are of broad interest to the physical chemistry community.
- [JCP](https://aip.scitation.org/journal/jcp) - focuses on advanced theoretical and computational methods of relevance to essentially all branches of chemical physics. Papers on software packages that implement chemical physics methods are also welcome. When to choose this journal?: new tools or methods that are of broad interest to the physical chemistry community.

### Top-tier journals

- [WIREs Computational Molecular Science](https://onlinelibrary.wiley.com/journal/17590884) -  promotes cross-disciplinary research on computational chemistry, biochemistry and materials science and provides authoritative, encyclopedic resources addressing key topics from diverse research perspectives. When to choose this journal?: new insights obtained by reframing and elucidating the links between a large number of works, some of which originated from <G|QC|G>.
- [Nature Communications](https://www.nature.com/ncomms/) - focuses on publishing high-quality research in biology, health, physics, chemistry, Earth sciences, and all related. When to choose this journal?: ground breaking work that is expected to have a large impact at the interface of multiple fields.
- [Nature Chemistry](https://www.nature.com/nchem/) - focuses on publishing high-quality papers that describe the most significant and cutting-edge research in all areas of chemistry. When to choose this journal?: ground breaking work that is expected to have a large impact in chemistry.
- [PRL](https://journals.aps.org/prl/about) - focuses on short, high-quality reports of the most influential developments and transformative ideas in the full arc of fundamental and interdisciplinary physics research. When to choose this journal?: ground breaking work that is expected to have a large impact in chemistry and physics.

## Writing cover letters

Example cover letter as [pdf](../media/cover-letter.pdf) and [docx](../media/cover-letter.docx)

- [Writing cover letters for scientific manuscripts](https://biosciencewriters.com/Writing-Cover-Letters-for-Scientific-Manuscripts.aspx)
- [Nature: how to write a cover letter](http://blogs.nature.com/methagora/2013/09/how-to-write-a-cover-letter.html)
- [Nature immunology: prelude to a good story](https://www.nature.com/articles/ni0208-107)
- [Springer: cover letters](https://www.springer.com/gp/authors-editors/authorandreviewertutorials/submitting-to-a-journal-and-peer-review/cover-letters/10285574)
- [How to write the best journal submission cover letter](https://wordvice.com/journal-submission-cover-letter/)

## Graphical TOC

Example [Graphical TOC](../media/TOC.pdf)

- [ACS Guidelines](../media/toc_abstract_graphics_guidelines.pdf)

## Writing rebuttal letters

- [How to write a rebuttal letter](http://blogs.nature.com/methagora/2013/09/how-to-write-a-rebuttal-letter.html)
- Example rebuttal letter as [docx](../media/rebuttal-letter.docx) and as [pdf](../media/rebuttal-letter.pdf)

## Abbreviations for journals

| Journal | Abbreviation |
| --- | --- |
| Chemical Physics Letters | Chem. Phys. Lett. |
| Chemical Reviews | Chem. Rev. |
| International Journal of Quantum Chemistry | Int. J. Quantum Chem. |
| Journal of Chemical Theory and Computation | J. Chem. Theory Comput. |
| Journal of Chemical Physics | J. Chem. Phys. |
| Journal of Mathematical Chemistry |  J. Math. Chem. |
| Journal of Molecular Modeling | J. Mol. Model. |
| Journal of Physics: Condensed Matter | J. Phys. Condens. Matter. |
| Journal of Physical Chemistry | J. Phys. Chem. |
| Molecular Physics | Mol. Phys. |
| Physical Chemistry Chemistry Physics | Phys. Chem. Chem. Phys. |
| Physical Review A | Phys. Rev. A |
| Physical Review Letters | Phys. Rev. Lett. |
| Theoretical Chemistry Accounts |  Theor. Chem. Acc. |
