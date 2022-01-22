from dft.util import VisualizeFourierTransform as vft
import argparse

parser = argparse.ArgumentParser(description='Visualize the fourier transform.')
parser.add_argument('-f','--freq',required=True,help='Comma seperated frequency values')
args = parser.parse_args()

if __name__=='__main__':
    f = args.freq.replace(' ','')
    f = f.split(',')
    f = list(map(int, f))
    
    ft = vft(f)
    ft.visualize()