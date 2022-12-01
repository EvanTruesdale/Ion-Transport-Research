#!/usr/bin/env python

import numpy as np
import pandas as pd
import random

name = 'LLZO_Ia3d'
filled_file = 'LLZO_Ia3d_filled.vasp'
supercell = (2,2,2)

# O:   96/96 O
# Zr:  16/16 Zr
# La:  24/24 La
# Li2: 32/96 Li, 64/96 Vac.
# Li1: 18/24 Li,  2/24 Al,  4/24 Vac.

LI1_sites = 24
LI2_sites = 96

with open(filled_file, 'r') as f:
    lines = f.readlines()

scale = lines[1]
lattice = lines[2:5]
composition = lines[5:7]
method = lines[7]
atomic_positions = lines[8:]

elements = np.array(composition[0].rstrip('\n').split(' '))
elements = elements[elements != '']
numbers = np.array(composition[1].rstrip('\n').split(' '))
numbers = numbers[numbers != '']
composition_dict = {elements[i]: numbers[i] for i in range(len(elements))}

atomic_positions_conv = np.array([x.rstrip('\n').split(" ") for x in atomic_positions])
atomic_positions_conv = np.array([x[x != ''] for x in atomic_positions_conv])
atomic_positions_conv = atomic_positions_conv.astype('float')

atomic_positions_dict = dict.fromkeys(elements)
s = 0
for element in elements:
    atomic_positions_dict[element] = atomic_positions_conv[s:s + int(composition_dict.get(element))]
    s = s + int(composition_dict.get(element))

octahedral_Li = atomic_positions_dict['Li'][LI1_sites:]
octahedral_Li_sort = np.empty((0,3))
while True:
    if octahedral_Li.size == 0:
        break
    v1 = octahedral_Li[0]
    min_dist = 1
    min_v2 = np.array([0,0,0])
    min_j = 1
    for j in np.arange(1, len(octahedral_Li)):
        v2 = octahedral_Li[j]
        dist = np.linalg.norm(v1-v2)
        if dist<min_dist:
            min_dist = dist
            min_v2 = v2.copy()
            min_j = j
    octahedral_Li_sort = np.append(octahedral_Li_sort, [v1], axis=0)
    octahedral_Li_sort = np.append(octahedral_Li_sort, [min_v2], axis=0)
    octahedral_Li = np.delete(octahedral_Li, [min_j,0], 0)

for config in range(2):
    
    lattice = lines[2:5]
    new_name = name + "_Al80_partial_" + f'{(config+1):01d}' + '.vasp'
    supercell_atomic_positions_dict = dict.fromkeys(elements)
    supercell_numbers = [0 for _ in elements]
    for element in elements:
        supercell_atomic_positions_dict[element] = np.array([[np.nan, np.nan, np.nan]])
        
    for x in range(supercell[0]):
        for y in range(supercell[1]):
            for z in range(supercell[2]):
                if (x+y+z)%2==0:
                    LI1_occupy = 0
                    AL_occupy = 8
                else:
                    LI1_occupy = 0
                    AL_occupy = 8
                LI2_occupy = 32

                new_atomic_positions_dict = dict.fromkeys(elements)
                new_atomic_positions_dict['O'] = atomic_positions_dict['O']
                new_atomic_positions_dict['Zr'] = atomic_positions_dict['Zr']
                new_atomic_positions_dict['La'] = atomic_positions_dict['La']

                lithiums = np.empty((0,3))
                aluminums = np.empty((0,3))

                # Octahedral lithium filling
                indices = np.arange(len(octahedral_Li_sort)//2)
                np.random.shuffle(indices)
                indices = indices[:LI2_occupy]
                for index in indices:
                    num = int(round(random.uniform(0,1), 0))
                    lithiums = np.append(lithiums, [octahedral_Li_sort[2*index + num]], axis=0)

                # Tetragonal site filling
                indices = np.arange(LI1_sites)
                np.random.shuffle(indices)
                for index in indices[:LI1_occupy]:
                    lithiums = np.append(lithiums, [atomic_positions_dict['Li'][index]], axis=0)
                new_atomic_positions_dict['Li'] = lithiums

                for index in indices[LI1_occupy:LI1_occupy+AL_occupy]:
                    aluminums = np.append(aluminums, [atomic_positions_dict['Al'][index]], axis=0)
                new_atomic_positions_dict['Al'] = aluminums

                new_composition_dict = {}
                for key, value in new_atomic_positions_dict.items():
                    new_composition_dict[key] = value.shape[0]
                elements = list(new_composition_dict.keys())
                numbers = list(new_composition_dict.values())
                for i, value in enumerate(numbers):
                    supercell_numbers[i] += value

                for element in elements:
                    shift = np.repeat([[x/supercell[0], y/supercell[1], z/supercell[2]]], new_atomic_positions_dict[element].shape[0], axis=0)
                    new_atomic_positions_dict[element] = (new_atomic_positions_dict[element]/np.array(supercell)) + shift
                    supercell_atomic_positions_dict[element] = np.append(supercell_atomic_positions_dict[element], new_atomic_positions_dict[element],axis=0)
    for element in elements:
        supercell_atomic_positions_dict[element] = supercell_atomic_positions_dict[element][~np.isnan(supercell_atomic_positions_dict[element])].reshape((-1,3))
    for i in range(3):
        lattice[i] = [float(x.strip('\n')) for x in lattice[i].split(' ') if x!='']
    lattice = lattice * np.array(supercell)

    with open(new_name, "w") as f:
        f.write(new_name+'\n')
        f.write(scale)
        f.write(" ".join([str(x) for x in lattice[0]])+'\n')
        f.write(" ".join([str(x) for x in lattice[1]])+'\n')
        f.write(" ".join([str(x) for x in lattice[2]])+'\n')
        f.write(" ".join(elements)+'\n')
        f.write(" ".join(np.array(supercell_numbers).astype('str'))+'\n')
        f.write(method)
        for key, value in supercell_atomic_positions_dict.items():
            rows = [' '.join(str(x) for x in line) for line in value]
            f.write('\n'.join(rows))
            f.write('\n')
