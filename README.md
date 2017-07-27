# Descriptions of the `parse_PDB_header`
A `Python 3` script for parsing the header information of PDB files.

  The main purpose of this script is to extract some of the header information, such as `Experiment Method`, `Resolution`, `R_free value`, `B-factor`, then calculate the grades of Resolution and R_free value based on the [grading of FirstGlance in Jmol](http://bioinformatics.org/firstglance/fgij/notes.htm#grading). Finally, saving above mentioned information as a `.csv` file (Pandas DataFrame). 

## Parameter used
`D`: The directory contains the PDB files.

## Usage
`python parse_PDB_header.py`
Then the program will ask you to input the directory that contains the PDB files. If you already at the directory, you only need to type `./` as input.
For example
~~~
python parse_PDB_header.py
~~~
<span style="color:blue">Please type the directory contains PDB files:   </span>
./

