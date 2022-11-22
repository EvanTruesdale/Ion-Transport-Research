# superfast_ion
Must make the following files:
POSCAR
KPOINTS
INCAR
POTCAR (cat /gscratch/cmt/software/vasp_PP/paw_PBE/[ELEMENT PP]/POTCAR > POTCAR)

cat /gscratch/cmt/software/vasp_PP/paw_PBE/O/POTCAR /gscratch/cmt/software/vasp_PP/paw_PBE/La/POTCAR /gscratch/cmt/software/vasp_PP/paw_PBE/Zr_sv/POTCAR /gscratch/cmt/software/vasp_PP/paw_PBE/Li/POTCAR /gscratch/cmt/software/vasp_PP/paw_PBE/Al/POTCAR > POTCAR

monitor LOOP in OUTCAR file while scaling with nodes

POTCAR has something wrong with the Zr file, always check that before running. VRHFIN =Zr, no space after equals sign

