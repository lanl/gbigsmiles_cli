import re
from dataclasses import dataclass, asdict 
import numpy as np 
import pandas as pd 

@dataclass 
class BigSmilesLabels:
    bigsmiles_label: str = "BigSMILES"
    mw_label: str = "Mw"
    mn_label: str = "Mn"
    frac_prefix: str = "f"
    full_dist_str: str = "log_normal"
    incomplete_dist_str: str = "gauss"

LABELS = BigSmilesLabels()

def get_distribution_strings(row:pd.Series,bigsmiles_label:str = LABELS.bigsmiles_label,mw_label = LABELS.mw_label,mn_label = LABELS.mn_label,frac_prefix:str = LABELS.frac_prefix,
                             full_dist_str: str =LABELS.full_dist_str,incomplete_dist_str: str = LABELS.incomplete_dist_str,half_width_factor:float = .1)->list[str|None]:
    '''
    Given a pandas Series, parses it to get the distribution component (i.e., |distribution_handle(x,y)|) of a Generative BigSMILES stirng.
    Args:
        row (pd.Series): 
        bigsmiles_label (str, optional): Defaults to LABELS.bigsmiles_label.
        mw_label (_type_, optional): Defaults to LABELS.mw_label.
        mn_label (_type_, optional): Defaults to LABELS.mn_label.
        frac_prefix (str, optional): Defaults to LABELS.frac_prefix.
            For copolymers, the label for the fraction of each copolymer before an index, starting from one. 
            E.g., a prefix of "f" for two copolymer blocks would be "f1", "f2". 
        full_dist_str (str, optional): Defaults to LABELS.full_dist_str.
            Default distribution to use when M_w and M_n are known.
        incomplete_dist_str (str, optional):  Defaults to LABELS.incomplete_dist_str.
            What distribution to use when the set of M_w, M_n is incomplete.
        half_width_factor (float, optional): Defaults to .1.
            Factor to fudge estimated half width for when it cannot be determined from available information.
    Returns:
        list[str|None]: 
    '''
    bigsmiles = row[bigsmiles_label]
    n_blocks = bigsmiles.count("{")
    tot_m_w = row[mw_label]
    tot_m_n = row[mn_label]
    
    dist_strs = []
    for i in range(n_blocks):
        try:
            fracs = row[[f"{frac_prefix}{int(i+1)}" for i in range(n_blocks)]]
            cur_frac = fracs.iloc[i]
        except:
            cur_frac = 1/n_blocks
        m_w, m_n = cur_frac*tot_m_w, cur_frac*tot_m_n 
        if not(np.isnan(m_w)) and not(np.isnan(m_n)):
            match full_dist_str:
                case "schulz_zimm"|"log_normal_mwn":
                    dist_str = f"|{full_dist_str}({int(round(m_w))}, {int(round(m_n))})|"
                case "schulz_zimm"|"log_normal":
                    dispersity = m_w/m_n 
                    dist_str = f"|{full_dist_str}({int(round(m_w))}, {round(dispersity,3)})|"
                case _ : 
                    raise ValueError(f"Invalid dist string {full_dist_str}")
        elif not(np.isnan(m_w)) or not(np.isnan(m_n)):
            m_x = np.nan_to_num(m_w,nan = 0)+np.nan_to_num(m_n,nan = 0)
            match incomplete_dist_str:
                case "gauss":
                    half_width_factor = half_width_factor*m_x
                    dist_str = f"|{incomplete_dist_str}({int(round(m_x))}, {int(round(half_width_factor))})|"
                case "uniform":
                    half_width  = half_width_factor*m_x
                    m_min, m_max = round(m_x-half_width), round(m_x+half_width)
                    dist_str = f"|{incomplete_dist_str}({int(round(m_min))}, {int(round(m_max))})|"
                case _:
                    raise ValueError("Invalid incomplete dist str")
        else: #unknown distribution
            dist_str = None 
        dist_strs.append(dist_str)
    return dist_strs

def split_bigsmiles(big_smiles:str)->list[str]:
    return re.findall(r"(\{?[^\{\}]+\}?)",big_smiles)

def is_stochastic(big_smiles_unit:str)->bool:
    '''Returns true if a BigSMILES instance has a stochastic unit'''
    return bool(re.match(r"\{.*\}",big_smiles_unit))

def get_gen_bigsmiles(row:pd.Series,**kwargs)->str:
    '''Given a Series containing polymer information and BigSMILES with labels as defined in kwargs, provides a corresponding Generative BigSMILES'''
    bigsmiles_label = kwargs.get("bigsmiles_label",LABELS.bigsmiles_label)
    bigsmiles = row[bigsmiles_label]
    bigsmiles_units = split_bigsmiles(bigsmiles)
    distribution_strings = get_distribution_strings(row,**kwargs)
    gen_bigsmiles = []
    dist_counter = 0
    for unit in bigsmiles_units:
        if is_stochastic(unit):
            full_unit = f"{unit}{distribution_strings[dist_counter]}"
            dist_counter = dist_counter + 1
        else:
            full_unit = unit 
        gen_bigsmiles.append(full_unit)
    return "".join(gen_bigsmiles)

def make_synthetic_gen_bigsmiles(bigsmiles:str,m_n_bounds:tuple[float],dispersity_bounds:tuple[float],**kwargs)->str:
    '''
    From a baseline BigSMILES, creates corresponding Generative BigSMILES with random values from within provided bounds.

    Args:
        bigsmiles (str): 
        m_n_bounds (tuple[float]): _
        dispersity_bounds (tuple[float]): 

    Returns:
       str
    '''
    bigsmiles_label = kwargs.get("bigsmiles_label",LABELS.bigsmiles_label)
    mw_label = kwargs.get("mw_label", LABELS.mw_label)
    mn_label = kwargs.get("mn_label", LABELS.mn_label)    
    m_n = np.random.random()*(m_n_bounds[-1]-m_n_bounds[0])+m_n_bounds[0]
    dispersity = np.random.random()*(dispersity_bounds[-1]-dispersity_bounds[0])+dispersity_bounds[0]
    m_w = dispersity*m_n

    bigsmiles_series = pd.Series({bigsmiles_label:bigsmiles,
                                  mw_label: m_w,
                                  mn_label: m_n})
    return get_gen_bigsmiles(bigsmiles_series,**kwargs)