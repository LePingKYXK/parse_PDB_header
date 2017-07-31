# Descriptions of the `parse_PDB_header`
A `Python 3` script for parsing the header information of PDB files.

  The main purpose of this script is to extract some of the header information, such as `Experiment Method`, `Resolution`, `R_free value`, `B-factor`, then calculate the grades of Resolution and R_free value based on the [grading of FirstGlance in Jmol](http://bioinformatics.org/firstglance/fgij/notes.htm#grading). Finally, saving above mentioned information as a `.csv` file (Pandas DataFrame). 


## Usage

For example
~~~
python parse_PDB_header.py
~~~
Then the program will ask you to input the directory that contains the PDB files. 
<p><span style="color:blue"><em>Please type the directory contains PDB files:</em>   </span></p>

If you already in that directory, you only need to type `./` as input.

### Acknowledgements
I thank [Wayne](https://github.com/fomightez) for discussion about the calc_R_free_grade() and deal_round() functions. 
I also would like to thank [Zachary Ware](http://bugs.python.org/issue24827?@ok_message=msg%20299498%20created%0Aissue%2024827%20message_count%2C%20messages%20edited%20ok&@template=item) for the detailed of the Decimal() function, which published on 2015-08-08 09:36.
