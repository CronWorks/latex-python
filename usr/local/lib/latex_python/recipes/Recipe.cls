%% Copyright (C) 2014 J Luke Scott
%% This material is subject to the LaTeX Project Public License. See
%% http://www.ctan.org/tex-archive/help/Catalogue/licenses.lppl.html for the details of that
%% license.

\usepackage{fontspec} %supports \setmainfont, \newfontfamily, OpenType
\setmainfont[Mapping=tex-text]{Charis SIL} % tex-text allows em dash
\setsansfont[Scale=MatchLowercase,Mapping=tex-text]{Open Sans}
\newfontfamily\tabularfont[Scale=0.8,Mapping=tex-text]{Open Sans}
\let\oldtabular\tabular
\let\endoldtabular\endtabular
\renewenvironment{tabular}{\tabularfont\oldtabular}{\endoldtabular}

\LoadClass[11pt,letterpaper]{article}


\usepackage[letterpaper]{geometry}
\geometry{
    verbose,
    tmargin=2.5cm,
    bmargin=2.5cm,
    lmargin=3cm,
    rmargin=3cm
}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt}

\usepackage{microtype}


\renewcommand{\section}{%
%   \@startsection{section}{level}{indent}{above>heading}{heading>text}{\bfseries}
    \@startsection{section}{1}{0pt}{7pt}{0.1pt}{\bfseries}
}

\AtBeginDocument{
    % don't show the page number
    \let\@oddfoot\@empty
}
