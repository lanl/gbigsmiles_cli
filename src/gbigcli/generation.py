import typer 
from typing_extensions import Annotated
import pandas as pd 
import rdkit.Chem 
import gbigsmiles


def check_entry(to_return = False)->None|str:
    '''
    Checks that the CLI entry works correctly
    Args:
        to_return (bool, optional):  Defaults to False.

    Returns:
        None|str: message
    '''
    msg = "You're running the gbigsmiles_cli"
    print(msg)
    if to_return:
        return msg 

def get_stochastic_samples(g_big_smiles: Annotated[str,typer.Argument(help="Provided base Gen BigSMILES for sampling")],
                           n: Annotated[int,typer.Argument(help = "Number of samples to generate")] = 1,
                           filename: Annotated[str|None,typer.Argument(help = "If provided, saves a .csv instead of printing to stdout")] = None,
                           print_conversion_errors: bool = False,
                           return_samples: bool = False)->None|list[str]:
    '''
    Provides a group of generated samples from a Generative BigSMILES (https://doi.org/10.1039/D3DD00147D) string.
    Args:
        g_big_smiles (Annotated[str,typer.Argument, optional): Generative BigSMILES string
        n (Annotated[int,typer.Argument, optional): number of samples to generate
        filename (Annotated[str | None,typer.Argument, optional): If provided, file output for generated samples
        print_conversion_errors (bool, optional): Defaults to False.
        return_samples (bool, optional): Defaults to False. 
            If True, returns generated samples as list[str]

    Returns:
        None|list[str]: If return_samples = True, the generated samples 
    '''
    stochastic_maker = gbigsmiles.BigSmiles.make(g_big_smiles)
    atomic_graph = stochastic_maker.get_generating_graph().get_atom_graph()
    samples = []
    for i in range(n):
        try:
            mol_graph = atomic_graph.sample_mol_graph()
            sample = rdkit.Chem.MolToSmiles(gbigsmiles.mol_graph_to_rdkit_mol(mol_graph))
        except Exception as err:
            if print_conversion_errors:
                print(repr(err))
            sample = ""
        samples.append(sample)
        if filename is None:
            print(sample)    
    if filename is not None: 
        df = pd.DataFrame({"g_big_smiles":samples})
        try:
            df.to_csv(filename)
        except Exception as err:
            print(repr(err))
    if return_samples:
        return samples 

