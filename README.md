# Descriptions of the `parse_PDB_header`
A `Python 3` script for parsing the header information of PDB files.

  The main purpose of this script is to extract some of the header information, such as `Experiment Method`, `Resolution`, `R value`, `R_free value`, `mean B-factor`, then calculate the grades of Resolution and R_free value based on the [grading of FirstGlance in Jmol](http://bioinformatics.org/firstglance/fgij/notes.htm#grading). Finally, saving above mentioned information as a `.csv` file (Pandas DataFrame). 

***Note**: In some PDB files (due to the complex of the protein's structure and the limitations of the experimental detections), the `R value` and `R_free value` have different data or NULL, even in the same PDB file. The `mean B-factor` some times reported as NULL*

**For examples:**

**In `1BRT.pdb`,**
<pre>
REMARK   3  FIT TO DATA USED IN REFINEMENT.                                     
REMARK   3   CROSS-VALIDATION METHOD          : THROUGHOUT                      
REMARK   3   FREE R VALUE TEST SET SELECTION  : RANDOM                          
<b>REMARK   3   R VALUE     (WORKING + TEST SET) : 0.140    </b>                       
<b>REMARK   3   R VALUE            (WORKING SET) : 0.147    </b>                     
REMARK   3   FREE R VALUE                     : 0.164                           
REMARK   3   FREE R VALUE TEST SET SIZE   (%) : 5.000                           
REMARK   3   FREE R VALUE TEST SET COUNT      : 2283                            
</pre>

**In `1GPD.pbd`**
<pre>
REMARK   3  FIT TO DATA USED IN REFINEMENT.                                     
REMARK   3   CROSS-VALIDATION METHOD          : NULL                            
REMARK   3   FREE R VALUE TEST SET SELECTION  : NULL                            
<b>REMARK   3   R VALUE            (WORKING SET) : NULL   </b>                         
<b>REMARK   3   FREE R VALUE                     : NULL   </b>                        
<b>REMARK   3   FREE R VALUE TEST SET SIZE   (%) : NULL   </b>
REMARK   3   FREE R VALUE TEST SET COUNT      : NULL                            
REMARK   3   ESTIMATED ERROR OF FREE R VALUE  : NULL     
...
REMARK   3  B VALUES.                                                           
REMARK   3   FROM WILSON PLOT           (A**2) : NULL                           
<b>REMARK   3   MEAN B VALUE      (OVERALL, A**2) : NULL   </b>                      
REMARK   3   OVERALL ANISOTROPIC B VALUE.                                       
REMARK   3    B11 (A**2) : NULL                                                 
REMARK   3    B22 (A**2) : NULL                                                 
REMARK   3    B33 (A**2) : NULL                                                 
REMARK   3    B12 (A**2) : NULL                                                 
REMARK   3    B13 (A**2) : NULL                                                 
REMARK   3    B23 (A**2) : NULL                                                 
</pre>

## Usage

For example
~~~
python parse_PDB_header.py
~~~
Then the program will ask you to input the directory that contains the PDB files. 
<p><span style="color:blue"><em>>>>Please type the directory contains PDB files:</em>   </span></p>

If you already in that directory, you only need to type `./` as input.

### Acknowledgements
I thank [Wayne](https://github.com/fomightez) for discussion about the `calc_R_free_grade()` and `deal_round()` functions. 
I also would like to thank [Zachary Ware](http://bugs.python.org/issue24827?@ok_message=msg%20299498%20created%0Aissue%2024827%20message_count%2C%20messages%20edited%20ok&@template=item) for the detailed of the `Decimal()` function, which published on 2015-08-08 09:36.
