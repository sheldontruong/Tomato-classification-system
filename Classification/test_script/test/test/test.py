from tensorflow.keras.models import load_model
import argparse
import tensorflow as tf
from utils import *

def main(args):
    #change dir and load model
    os.chdir(args.workingdir)
    model = load_model(args.modelpath) 
    #get session of model to use in gradCAM computing
    sess = tf.keras.backend.get_session()
    #run real time process
    test_vid("camera",model,sess)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--workingdir",default=".",help="current working directory")
    parser.add_argument("--modelpath",default = None,help = "model path")
    args = parser.parse_args()
    main(args)

